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

from msrest.serialization import Model


class Operation(Model):
    """REST API operation supported by CommunicationService resource provider.

    :param name: Name of the operation with format:
     {provider}/{resource}/{operation}
    :type name: str
    :param display: The object that describes the operation.
    :type display: ~microsoft.communication.models.OperationDisplay
    :param origin: Optional. The intended executor of the operation; governs
     the display of the operation in the RBAC UX and the audit logs UX.
    :type origin: str
    :param properties: Extra properties for the operation.
    :type properties: ~microsoft.communication.models.OperationProperties
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'display': {'key': 'display', 'type': 'OperationDisplay'},
        'origin': {'key': 'origin', 'type': 'str'},
        'properties': {'key': 'properties', 'type': 'OperationProperties'},
    }

    def __init__(self, **kwargs):
        super(Operation, self).__init__(**kwargs)
        self.name = kwargs.get('name', None)
        self.display = kwargs.get('display', None)
        self.origin = kwargs.get('origin', None)
        self.properties = kwargs.get('properties', None)
