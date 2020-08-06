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
    """Azure Communication Services User Management client.
    """
    
    def __init__(
        self, host, # type: str
        access_key, # type: str
        **kwargs # type: Any
         ):
        try:
            if not host.lower().startswith('http'):
                host = "https://" + host
        except AttributeError:
            raise ValueError("Account URL must be a string.")

        if not access_key:
            raise ValueError("You need to provide either a SAS token or an account shared key to authenticate.")
        
        super(UserManagementClient, self).__init__(**kwargs)

        self.api_version = '2020-07-20-preview1'
        auth_policy = HMACCredentialsPolicy(host, access_key)

        self.config = UserTokenManagementServiceConfiguration(authentication_policy=auth_policy ,logging_enable=True, **kwargs)
        self._client = AsyncPipelineClient(base_url=host, config=self.config, verify=False, **kwargs)
        self.user_management = UserManagementOperations(
            self._client, self._config, self._serialize, self._deserialize)
