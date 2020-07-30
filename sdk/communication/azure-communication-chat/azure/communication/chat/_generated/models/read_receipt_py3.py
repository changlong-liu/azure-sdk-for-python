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


class ReadReceipt(Model):
    """ReadReceipt.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar user_id: Read receipt sender id.
    :vartype user_id: str
    :ivar message_id: Id for the message that has been read. This id is server
     generated.
    :vartype message_id: str
    :ivar read_timestamp: Read receipt timestamp.
    :vartype read_timestamp: long
    :ivar client_message_id: Client message id specified in the
     Microsoft.AzureCommunicationService.Gateway.Models.Client.CreateMessageRequest.
     This Id is a client-specific Id in a numeric unsigned Int64 format. It can
     be used for client deduping, among other client usages.
    :vartype client_message_id: str
    """

    _validation = {
        'user_id': {'readonly': True},
        'message_id': {'readonly': True},
        'read_timestamp': {'readonly': True},
        'client_message_id': {'readonly': True},
    }

    _attribute_map = {
        'user_id': {'key': 'userId', 'type': 'str'},
        'message_id': {'key': 'messageId', 'type': 'str'},
        'read_timestamp': {'key': 'readTimestamp', 'type': 'long'},
        'client_message_id': {'key': 'clientMessageId', 'type': 'str'},
    }

    def __init__(self, **kwargs) -> None:
        super(ReadReceipt, self).__init__(**kwargs)
        self.user_id = None
        self.message_id = None
        self.read_timestamp = None
        self.client_message_id = None
