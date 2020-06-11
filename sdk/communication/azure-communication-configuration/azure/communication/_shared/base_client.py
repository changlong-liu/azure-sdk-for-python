# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from typing import (  # pylint: disable=unused-import
    cast,
    Union,
    Optional,
    Any,
    Iterable,
    Dict,
    List,
    Type,
    Tuple,
    TYPE_CHECKING,
)

import logging

try:
    from urllib.parse import parse_qs, quote
except ImportError:
    from urlparse import parse_qs  # type: ignore
    from urllib2 import quote  # type: ignore

import six

from azure.core.pipeline.transport import HttpTransport
from azure.core.pipeline.policies import (
    RedirectPolicy,
    ContentDecodePolicy,
    BearerTokenCredentialPolicy,
    ProxyPolicy,
    DistributedTracingPolicy,
    HttpLoggingPolicy,
)

from .constants import STORAGE_OAUTH_SCOPE, SERVICE_HOST_BASE, CONNECTION_TIMEOUT, READ_TIMEOUT
from .models import LocationMode
from .authentication import SharedKeyCredentialPolicy
from .shared_access_signature import QueryStringConstants


_LOGGER = logging.getLogger(__name__)
_SERVICE_PARAMS = {
    "blob": {"primary": "BlobEndpoint", "secondary": "BlobSecondaryEndpoint"},
    "queue": {"primary": "QueueEndpoint", "secondary": "QueueSecondaryEndpoint"},
    "file": {"primary": "FileEndpoint", "secondary": "FileSecondaryEndpoint"},
    "dfs": {"primary": "BlobEndpoint", "secondary": "BlobSecondaryEndpoint"},
}


class StorageAccountHostsMixin(object):  # pylint: disable=too-many-instance-attributes
    def __init__(
        self,
        parsed_url,  # type: Any
        service,  # type: str
        credential=None,  # type: Optional[Any]
        **kwargs  # type: Any
    ):
        # type: (...) -> None
        self._location_mode = kwargs.get("_location_mode", LocationMode.PRIMARY)
        self._hosts = kwargs.get("_hosts")
        self.scheme = parsed_url.scheme

        if service not in ["blob", "queue", "file-share", "dfs"]:
            raise ValueError("Invalid service: {}".format(service))
        service_name = service.split('-')[0]
        account = parsed_url.netloc.split(".{}.core.".format(service_name))
        self.account_name = account[0] if len(account) > 1 else None
        secondary_hostname = None

        self.credential = format_shared_key_credential(account, credential)
        if self.scheme.lower() != "https" and hasattr(self.credential, "get_token"):
            raise ValueError("Token credential is only supported with HTTPS.")
        if hasattr(self.credential, "account_name"):
            self.account_name = self.credential.account_name
            secondary_hostname = "{}-secondary.{}.{}".format(
                self.credential.account_name, service_name, SERVICE_HOST_BASE)

        if not self._hosts:
            if len(account) > 1:
                secondary_hostname = parsed_url.netloc.replace(account[0], account[0] + "-secondary")
            if kwargs.get("secondary_hostname"):
                secondary_hostname = kwargs["secondary_hostname"]
            primary_hostname = (parsed_url.netloc + parsed_url.path).rstrip('/')
            self._hosts = {LocationMode.PRIMARY: primary_hostname, LocationMode.SECONDARY: secondary_hostname}

        self.require_encryption = kwargs.get("require_encryption", False)
        self.key_encryption_key = kwargs.get("key_encryption_key")
        self.key_resolver_function = kwargs.get("key_resolver_function")
        self._config, self._pipeline = self._create_pipeline(self.credential, storage_sdk=service, **kwargs)

    def __enter__(self):
        self._client.__enter__()
        return self

    def __exit__(self, *args):
        self._client.__exit__(*args)

    def close(self):
        """ This method is to close the sockets opened by the client.
        It need not be used when using with a context manager.
        """
        self._client.close()

    @property
    def url(self):
        """The full endpoint URL to this entity, including SAS token if used.

        This could be either the primary endpoint,
        or the secondary endpoint depending on the current :func:`location_mode`.
        """
        return self._format_url(self._hosts[self._location_mode])

    @property
    def primary_endpoint(self):
        """The full primary endpoint URL.

        :type: str
        """
        return self._format_url(self._hosts[LocationMode.PRIMARY])

    @property
    def primary_hostname(self):
        """The hostname of the primary endpoint.

        :type: str
        """
        return self._hosts[LocationMode.PRIMARY]

    @property
    def secondary_endpoint(self):
        """The full secondary endpoint URL if configured.

        If not available a ValueError will be raised. To explicitly specify a secondary hostname, use the optional
        `secondary_hostname` keyword argument on instantiation.

        :type: str
        :raise ValueError:
        """
        if not self._hosts[LocationMode.SECONDARY]:
            raise ValueError("No secondary host configured.")
        return self._format_url(self._hosts[LocationMode.SECONDARY])

    @property
    def secondary_hostname(self):
        """The hostname of the secondary endpoint.

        If not available this will be None. To explicitly specify a secondary hostname, use the optional
        `secondary_hostname` keyword argument on instantiation.

        :type: str or None
        """
        return self._hosts[LocationMode.SECONDARY]

    @property
    def location_mode(self):
        """The location mode that the client is currently using.

        By default this will be "primary". Options include "primary" and "secondary".

        :type: str
        """

        return self._location_mode

    @location_mode.setter
    def location_mode(self, value):
        if self._hosts.get(value):
            self._location_mode = value
            self._client._config.url = self.url  # pylint: disable=protected-access
        else:
            raise ValueError("No host URL for location mode: {}".format(value))

    @property
    def api_version(self):
        """The version of the Storage API used for requests.

        :type: str
        """
        return self._client._config.version  # pylint: disable=protected-access

    def _format_query_string(self, sas_token, credential, snapshot=None, share_snapshot=None):
        query_str = "?"
        if snapshot:
            query_str += "snapshot={}&".format(self.snapshot)
        if share_snapshot:
            query_str += "sharesnapshot={}&".format(self.snapshot)
        if sas_token and not credential:
            query_str += sas_token
        elif is_credential_sastoken(credential):
            query_str += credential.lstrip("?")
            credential = None
        return query_str.rstrip("?&"), credential


class TransportWrapper(HttpTransport):
    """Wrapper class that ensures that an inner client created
    by a `get_client` method does not close the outer transport for the parent
    when used in a context manager.
    """
    def __init__(self, transport):
        self._transport = transport

    def send(self, request, **kwargs):
        return self._transport.send(request, **kwargs)

    def open(self):
        pass

    def close(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, *args):  # pylint: disable=arguments-differ
        pass


def format_shared_key_credential(account, credential):
    if isinstance(credential, six.string_types):
        if len(account) < 2:
            raise ValueError("Unable to determine account name for shared key credential.")
        credential = {"account_name": account[0], "account_key": credential}
    if isinstance(credential, dict):
        if "account_name" not in credential:
            raise ValueError("Shared key credential missing 'account_name")
        if "account_key" not in credential:
            raise ValueError("Shared key credential missing 'account_key")
        return SharedKeyCredentialPolicy(**credential)
    return credential


def parse_connection_str(conn_str):
    # type: (str) -> Tuple[str, str, str, str]
    endpoint = None
    shared_access_key = None
    for element in conn_str.split(";"):
        key, _, value = element.partition("=")
        if key.lower() == "endpoint":
            endpoint = value.rstrip("/")
        elif key.lower() == "accesskey":
            shared_access_key = value
    if not all([endpoint, shared_access_key]):
        raise ValueError(
            "Invalid connection string. Should be in the format: "
            "endpoint=sb://<FQDN>/;accesskey=<KeyValue>"
        )
    left_slash_pos = cast(str, endpoint).find("//")
    if left_slash_pos != -1:
        host = cast(str, endpoint)[left_slash_pos + 2:]
    else:
        host = str(endpoint)
    
    return host, str(shared_access_key)


def parse_query(query_str):
    sas_values = QueryStringConstants.to_list()
    parsed_query = {k: v[0] for k, v in parse_qs(query_str).items()}
    sas_params = ["{}={}".format(k, quote(v, safe='')) for k, v in parsed_query.items() if k in sas_values]
    sas_token = None
    if sas_params:
        sas_token = "&".join(sas_params)

    snapshot = parsed_query.get("snapshot") or parsed_query.get("sharesnapshot")
    return snapshot, sas_token


def is_credential_sastoken(credential):
    if not credential or not isinstance(credential, six.string_types):
        return False

    sas_values = QueryStringConstants.to_list()
    parsed_query = parse_qs(credential.lstrip("?"))
    if parsed_query and all([k in sas_values for k in parsed_query.keys()]):
        return True
    return False
