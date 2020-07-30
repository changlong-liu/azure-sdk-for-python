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


class ThreadMember(Model):
    """A member of the thread.

    All required parameters must be populated in order to send to Azure.

    :param id: Required. The id of the thread member in the format
     `8:acs:ResourceId_AcsUserId`.
    :type id: str
    :param display_name: Display name for the thread member.
    :type display_name: str
    :param member_role: Required. Possible values include: 'Admin', 'User'
    :type member_role: str or ~azure.communication.chat.models.MemberRole
    :param share_history_time: Time from which the group chat history is
     shared with the member in EPOCH time (milliseconds).
     Possible values:
     - `0` which means share everything
     - `-1` which means share nothing
     - `1594691284031` which is epoch time equivalent to 7/14/2020 1:48:04 AM
     +00:00
    :type share_history_time: str
    """

    _validation = {
        'id': {'required': True},
        'member_role': {'required': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'display_name': {'key': 'displayName', 'type': 'str'},
        'member_role': {'key': 'memberRole', 'type': 'str'},
        'share_history_time': {'key': 'shareHistoryTime', 'type': 'str'},
    }

    def __init__(self, *, id: str, member_role, display_name: str=None, share_history_time: str=None, **kwargs) -> None:
        super(ThreadMember, self).__init__(**kwargs)
        self.id = id
        self.display_name = display_name
        self.member_role = member_role
        self.share_history_time = share_history_time
