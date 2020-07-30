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


class CreateMessageRequest(Model):
    """CreateMessageRequest.

    All required parameters must be populated in order to send to Azure.

    :param client_message_id: This Id is a client-specific Id in a numeric
     unsigned Int64 format. It can be used for client deduping, among other
     client usages.
    :type client_message_id: str
    :param priority: Possible values include: 'Normal', 'High'
    :type priority: str or ~azure.communication.chat.models.MessagePriority
    :param content: Required. Chat message content.
    :type content: str
    :param sender_display_name: The display name of the message sender. This
     property is used to populate sender name for push notifications.
    :type sender_display_name: str
    """

    _validation = {
        'content': {'required': True},
    }

    _attribute_map = {
        'client_message_id': {'key': 'clientMessageId', 'type': 'str'},
        'priority': {'key': 'priority', 'type': 'str'},
        'content': {'key': 'content', 'type': 'str'},
        'sender_display_name': {'key': 'senderDisplayName', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(CreateMessageRequest, self).__init__(**kwargs)
        self.client_message_id = kwargs.get('client_message_id', None)
        self.priority = kwargs.get('priority', None)
        self.content = kwargs.get('content', None)
        self.sender_display_name = kwargs.get('sender_display_name', None)
