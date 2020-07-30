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


class AddThreadMembersRequest(Model):
    """AddThreadMembersRequest.

    All required parameters must be populated in order to send to Azure.

    :param members: Required. Members to add to a thread.
    :type members: list[~azure.communication.chat.models.ThreadMember]
    """

    _validation = {
        'members': {'required': True},
    }

    _attribute_map = {
        'members': {'key': 'members', 'type': '[ThreadMember]'},
    }

    def __init__(self, *, members, **kwargs) -> None:
        super(AddThreadMembersRequest, self).__init__(**kwargs)
        self.members = members
