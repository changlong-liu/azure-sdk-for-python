from urllib.parse import urlparse
from azure.communication import UserTokenOperations
from msrest import Serializer, Deserializer
from msrest.service_client import ServiceClient
from azure.core.pipeline import policies
from azure.core import PipelineClient
from ._shared.base_client import parse_connection_str, parse_query
from ._generated import models
from ._generated._configuration import UserTokenManagementServiceConfiguration


class UserTokenClient(UserTokenOperations):
    """User JWT Token client.
    """
    
    @classmethod
    def from_connection_string(
            cls, conn_str,  # type: str
            credentials=None,  # type: Optional[Any]
            **kwargs  # type: Any
        ):  # type: (...) -> UserTokenClient
        """Create UserTokenClient from a Connection String.

        :param str conn_str:
            A connection string to an Azure Communication Service resource.
        :param credential:
            The credentials with which to authenticate. This is optional if the
            account URL already has a SAS token, or the connection string already has shared
            access key values. The value can be a SAS token string, an account shared access
            key, or an instance of a TokenCredentials class from azure.identity.
            Credentials provided here will take precedence over those in the connection string.
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
        endpoint_url, credentials = parse_connection_str(conn_str)

        return cls(endpoint_url, credentials, **kwargs)

    def __init__(self, endpoint_url, credentials, **kwargs):
        try:
            if not endpoint_url.lower().startswith('http'):
                endpoint_url = "https://" + endpoint_url
        except AttributeError:
            raise ValueError("Account URL must be a string.")
        parsed_url = urlparse(endpoint_url.rstrip('/'))

        _, sas_token = parse_query(parsed_url.query)
        if not sas_token and not credentials:
            raise ValueError("You need to provide either a SAS token or an account shared key to authenticate.")
        
        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self.config = UserTokenManagementServiceConfiguration(credentials, logging_enable=True, **kwargs)
        self.api_version = '2020-06-04-preview'
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)
        self._client = PipelineClient(base_url=endpoint_url, config=self.config, verify=False, **kwargs) 

        super(UserTokenClient, self).__init__(self._client, self.config, self._serialize, self._deserialize)