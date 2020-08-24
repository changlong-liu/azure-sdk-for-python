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


class CommunicationServiceResource(Model):
    """A class representing a CommunicationService resource.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar id: Fully qualified resource ID for the resource.
    :vartype id: str
    :ivar name: The name of the resource.
    :vartype name: str
    :ivar type: The type of the service - e.g.
     "Microsoft.Communication/CommunicationServices"
    :vartype type: str
    :param location: The Azure location where the CommunicationService is
     running.
    :type location: str
    :param tags: Tags of the service which is a list of key value pairs that
     describe the resource.
    :type tags: dict[str, str]
    :ivar provisioning_state: Provisioning state of the resource. Possible
     values include: 'Unknown', 'Succeeded', 'Failed', 'Canceled', 'Running',
     'Creating', 'Updating', 'Deleting', 'Moving'
    :vartype provisioning_state: str or
     ~microsoft.communication.models.ProvisioningState
    :ivar host_name: FQDN of the CommunicationService instance.
    :vartype host_name: str
    :param push_notification_credentials: Credentials used to enable push
     notifications. Setting any credential set will enable push notifications.
    :type push_notification_credentials:
     ~microsoft.communication.models.PushNotificationCredentials
    :ivar version: Version of the CommunicationService resource. Probably you
     need the same or higher version of client SDKs.
    :vartype version: str
    :ivar immutable_resource_id: The immutable resource Id of the Spool
     resource.
    :vartype immutable_resource_id: str
    """

    _validation = {
        'id': {'readonly': True},
        'name': {'readonly': True},
        'type': {'readonly': True},
        'provisioning_state': {'readonly': True},
        'host_name': {'readonly': True},
        'version': {'readonly': True},
        'immutable_resource_id': {'readonly': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
        'location': {'key': 'location', 'type': 'str'},
        'tags': {'key': 'tags', 'type': '{str}'},
        'provisioning_state': {'key': 'properties.provisioningState', 'type': 'str'},
        'host_name': {'key': 'properties.hostName', 'type': 'str'},
        'push_notification_credentials': {'key': 'properties.pushNotificationCredentials', 'type': 'PushNotificationCredentials'},
        'version': {'key': 'properties.version', 'type': 'str'},
        'immutable_resource_id': {'key': 'properties.immutableResourceId', 'type': 'str'},
    }

    def __init__(self, *, location: str=None, tags=None, push_notification_credentials=None, **kwargs) -> None:
        super(CommunicationServiceResource, self).__init__(**kwargs)
        self.id = None
        self.name = None
        self.type = None
        self.location = location
        self.tags = tags
        self.provisioning_state = None
        self.host_name = None
        self.push_notification_credentials = push_notification_credentials
        self.version = None
        self.immutable_resource_id = None
