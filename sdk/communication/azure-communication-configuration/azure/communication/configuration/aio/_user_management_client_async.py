# coding=utf-8
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

from azure.core import AsyncPipelineClient
from .._generated.aio._user_token_management_service_async  import UserTokenManagementService
from .._generated.aio._configuration_async  import UserTokenManagementServiceConfiguration
from .._generated.aio.operations_async import UserManagementOperations
from .._shared.policy import HMACCredentialsPolicy
from .._user_management_client import UserManagementClient as UserManagementClientBase

class UserManagementClient(UserTokenManagementService, UserManagementClientBase):
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
            **kwargs # type: Any
        ):
        # type: (...) -> None
        try:
            if not host.lower().startswith('http'):
                host = "https://" + host
        except AttributeError:
            raise ValueError("Account URL must be a string.")

        if not credential:
            raise ValueError("You need to an account shared key to authenticate.")

        super(UserManagementClient, self).__init__(**kwargs)

        self.api_version = '2020-07-20-preview1'
        auth_policy = HMACCredentialsPolicy(host, credential)

        self.config = UserTokenManagementServiceConfiguration(\
            authentication_policy=auth_policy, **kwargs)
        self._client = AsyncPipelineClient(base_url=host,\
            config=self.config, **kwargs)
        self.user_management = UserManagementOperations(
            self._client, self._config, self._serialize, self._deserialize)
