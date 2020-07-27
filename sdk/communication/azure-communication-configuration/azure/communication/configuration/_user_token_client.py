from urllib.parse import urlparse
from ._generated.operations._user_management_operations import UserManagementOperations
from msrest import Serializer, Deserializer
from azure.core import PipelineClient
from ._shared.base_client import parse_connection_str, parse_query
from ._shared.policy import HMACCredentialsPolicy
from ._generated import models
from ._generated._configuration import UserTokenManagementServiceConfiguration


class UserTokenClient(UserManagementOperations):
    """User JWT Token client.
    """
    
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
        parsed_url = urlparse(host.rstrip('/'))

        _, sas_token = parse_query(parsed_url.query)
        if not sas_token and not access_key:
            raise ValueError("You need to provide either a SAS token or an account shared key to authenticate.")
        
        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        auth_policy = HMACCredentialsPolicy(host, access_key)

        self.config = UserTokenManagementServiceConfiguration(authentication_policy=auth_policy ,logging_enable=True, **kwargs)
        self.api_version = '2020-06-04-preview'
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)
        self._client = PipelineClient(base_url=host, config=self.config, verify=False, **kwargs) 

        super(UserTokenClient, self).__init__(self._client, self.config, self._serialize, self._deserialize)