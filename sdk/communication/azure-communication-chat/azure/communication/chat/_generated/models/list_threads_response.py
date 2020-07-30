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


class ListThreadsResponse(Model):
    """ListThreadsResponse.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar threads: List of threads.
    :vartype threads: list[~azure.communication.chat.models.ThreadInfo]
    :ivar sync_state: Continuation link to get new and modified threads.
    :vartype sync_state: str
    :ivar backward_link: If there are more threads that can be retrieved, the
     backward link will be populated.
    :vartype backward_link: str
    """

    _validation = {
        'threads': {'readonly': True},
        'sync_state': {'readonly': True},
        'backward_link': {'readonly': True},
    }

    _attribute_map = {
        'threads': {'key': 'threads', 'type': '[ThreadInfo]'},
        'sync_state': {'key': 'syncState', 'type': 'str'},
        'backward_link': {'key': 'backwardLink', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(ListThreadsResponse, self).__init__(**kwargs)
        self.threads = None
        self.sync_state = None
        self.backward_link = None
