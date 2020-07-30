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


class ListMessagesResponse(Model):
    """ListMessagesResponse.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar messages: List of messages.
    :vartype messages: list[~azure.communication.chat.models.Message]
    :ivar sync_state: Continuation link to get new and modified messages.
    :vartype sync_state: str
    :ivar backward_link: If there are more messages that can be retrieved, the
     backward link will be populated.
    :vartype backward_link: str
    """

    _validation = {
        'messages': {'readonly': True},
        'sync_state': {'readonly': True},
        'backward_link': {'readonly': True},
    }

    _attribute_map = {
        'messages': {'key': 'messages', 'type': '[Message]'},
        'sync_state': {'key': 'syncState', 'type': 'str'},
        'backward_link': {'key': 'backwardLink', 'type': 'str'},
    }

    def __init__(self, **kwargs) -> None:
        super(ListMessagesResponse, self).__init__(**kwargs)
        self.messages = None
        self.sync_state = None
        self.backward_link = None
