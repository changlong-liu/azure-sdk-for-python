# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.service_client import SDKClient
from msrest import Serializer, Deserializer

from ._configuration import AzureDigitalTwinsManagementClientConfiguration
from .operations import DigitalTwinsOperations
from .operations import DigitalTwinsEndpointOperations
from .operations import Operations
from . import models


class AzureDigitalTwinsManagementClient(SDKClient):
    """Azure Digital Twins Client for managing DigitalTwinsInstance

    :ivar config: Configuration for client.
    :vartype config: AzureDigitalTwinsManagementClientConfiguration

    :ivar digital_twins: DigitalTwins operations
    :vartype digital_twins: azure.mgmt.digitaltwins.operations.DigitalTwinsOperations
    :ivar digital_twins_endpoint: DigitalTwinsEndpoint operations
    :vartype digital_twins_endpoint: azure.mgmt.digitaltwins.operations.DigitalTwinsEndpointOperations
    :ivar operations: Operations operations
    :vartype operations: azure.mgmt.digitaltwins.operations.Operations

    :param credentials: Credentials needed for the client to connect to Azure.
    :type credentials: :mod:`A msrestazure Credentials
     object<msrestazure.azure_active_directory>`
    :param subscription_id: The subscription identifier.
    :type subscription_id: str
    :param str base_url: Service URL
    """

    def __init__(
            self, credentials, subscription_id, base_url=None):

        self.config = AzureDigitalTwinsManagementClientConfiguration(credentials, subscription_id, base_url)
        super(AzureDigitalTwinsManagementClient, self).__init__(self.config.credentials, self.config)

        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self.api_version = '2020-10-31'
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)

        self.digital_twins = DigitalTwinsOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.digital_twins_endpoint = DigitalTwinsEndpointOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.operations = Operations(
            self._client, self.config, self._serialize, self._deserialize)
