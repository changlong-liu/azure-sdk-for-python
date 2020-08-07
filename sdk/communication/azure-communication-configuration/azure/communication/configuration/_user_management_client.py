# coding=utf-8
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

from azure.core import PipelineClient
from ._generated import UserTokenManagementService
from ._generated.operations import UserManagementOperations
from ._shared.utils import parse_connection_str
from ._shared.policy import HMACCredentialsPolicy
from ._generated._configuration import UserTokenManagementServiceConfiguration


class UserManagementClient(UserTokenManagementService):
    """Azure Communication Services(ACS) User Management client.

    :param str host:
        The host url for ACS resource.
    :param credential:
        The credentials with which to authenticate. The value is an account
        shared access key

    .. admonition:: Example:

        .. literalinclude:: ../samples/configuration_sample_usertoken_issue.py
            :language: python
            :dedent: 8
            :caption: Creating the BlobClient from a URL to a public blob (no auth needed).
    """
    def __init__(
            self, host, # type: str
            credential, # type: str
            logging_enable=False, # type: bool
            **kwargs # type: Any
        ):
        # type: (...) -> None
        try:
            if not host.lower().startswith('http'):
                host = "https://" + host
        except AttributeError:
            raise ValueError("Account URL must be a string.")

        if not credential:
            raise ValueError(
                "You need to provide account shared key to authenticate.")

        super(UserManagementClient, self).__init__(**kwargs)

        self.api_version = '2020-07-20-preview1'
        auth_policy = HMACCredentialsPolicy(host, credential)

        self._config = UserTokenManagementServiceConfiguration(authentication_policy=auth_policy,\
            logging_enable=logging_enable, **kwargs)
        self._client = PipelineClient(base_url=host, config=self._config, **kwargs)
        self.user_management = UserManagementOperations(
            self._client, self._config, self._serialize, self._deserialize)

    @classmethod
    def from_connection_string(
            cls, conn_str,  # type: str
            **kwargs  # type: Any
        ):  # type: (...) -> UserTokenClient
        """Create UserTokenClient from a Connection String.

        :param str conn_str:
            A connection string to an Azure Communication Service resource.
        :returns: A UserTokenClient.
        :rtype: ~azure.communication.UserTokenClient

        .. admonition:: Example:

            .. literalinclude:: ../samples/configuration_sample_usertoken_issue.py
                :start-after: [START auth_from_connection_string]
                :end-before: [END auth_from_connection_string]
                :language: python
                :dedent: 8
                :caption: Creating the UserTokenClient from a connection string.
        """
        host, access_key = parse_connection_str(conn_str)

        return cls(host, access_key, **kwargs)
