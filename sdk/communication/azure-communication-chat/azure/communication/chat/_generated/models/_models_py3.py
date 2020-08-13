# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from typing import List, Optional, Union

import msrest.serialization

from ._azure_communication_chat_service_enums import *


class AddThreadMembersRequest(msrest.serialization.Model):
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

    def __init__(
        self,
        *,
        members: List["ThreadMember"],
        **kwargs
    ):
        super(AddThreadMembersRequest, self).__init__(**kwargs)
        self.members = members


class CreateMessageRequest(msrest.serialization.Model):
    """CreateMessageRequest.

    All required parameters must be populated in order to send to Azure.

    :param client_message_id: This Id is a client-specific Id in a numeric unsigned Int64 format.
     It can be used for client deduping, among other client usages.
    :type client_message_id: str
    :param priority:  Possible values include: "Normal", "High".
    :type priority: str or ~azure.communication.chat.models.MessagePriority
    :param content: Required. Chat message content.
    :type content: str
    :param sender_display_name: The display name of the message sender. This property is used to
     populate sender name for push notifications.
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

    def __init__(
        self,
        *,
        content: str,
        client_message_id: Optional[str] = None,
        priority: Optional[Union[str, "MessagePriority"]] = None,
        sender_display_name: Optional[str] = None,
        **kwargs
    ):
        super(CreateMessageRequest, self).__init__(**kwargs)
        self.client_message_id = client_message_id
        self.priority = priority
        self.content = content
        self.sender_display_name = sender_display_name


class CreateMessageResponse(msrest.serialization.Model):
    """CreateMessageResponse.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar id: The Id of the message. This Id is server generated.
    :vartype id: str
    :ivar client_message_id: This Id is a client-specific Id in a numeric unsigned Int64 format. It
     can be used for client deduping, among other client usages.
    :vartype client_message_id: str
    """

    _validation = {
        'id': {'readonly': True},
        'client_message_id': {'readonly': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'client_message_id': {'key': 'clientMessageId', 'type': 'str'},
    }

    def __init__(
        self,
        **kwargs
    ):
        super(CreateMessageResponse, self).__init__(**kwargs)
        self.id = None
        self.client_message_id = None


class CreateThreadRequest(msrest.serialization.Model):
    """CreateThreadRequest.

    All required parameters must be populated in order to send to Azure.

    :param topic: Required. The thread topic.
    :type topic: str
    :param is_sticky_thread: Flag if a thread is sticky - sticky thread has an immutable member
     list, members cannot be added or removed.
     Sticky threads are only supported for 1-1 chat, i.e. with only two members.
    :type is_sticky_thread: bool
    :param members: Required. Members to be added to the thread.
    :type members: list[~azure.communication.chat.models.ThreadMember]
    """

    _validation = {
        'topic': {'required': True},
        'members': {'required': True},
    }

    _attribute_map = {
        'topic': {'key': 'topic', 'type': 'str'},
        'is_sticky_thread': {'key': 'isStickyThread', 'type': 'bool'},
        'members': {'key': 'members', 'type': '[ThreadMember]'},
    }

    def __init__(
        self,
        *,
        topic: str,
        members: List["ThreadMember"],
        is_sticky_thread: Optional[bool] = None,
        **kwargs
    ):
        super(CreateThreadRequest, self).__init__(**kwargs)
        self.topic = topic
        self.is_sticky_thread = is_sticky_thread
        self.members = members


class CreateThreadResponse(msrest.serialization.Model):
    """CreateThreadResponse.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar id: Thread Id.
    :vartype id: str
    """

    _validation = {
        'id': {'readonly': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
    }

    def __init__(
        self,
        **kwargs
    ):
        super(CreateThreadResponse, self).__init__(**kwargs)
        self.id = None


class ListMessagesResponse(msrest.serialization.Model):
    """ListMessagesResponse.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar messages: List of messages.
    :vartype messages: list[~azure.communication.chat.models.Message]
    :ivar sync_state: Continuation link to get new and modified messages.
    :vartype sync_state: str
    :ivar backward_link: If there are more messages that can be retrieved, the backward link will
     be populated.
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

    def __init__(
        self,
        **kwargs
    ):
        super(ListMessagesResponse, self).__init__(**kwargs)
        self.messages = None
        self.sync_state = None
        self.backward_link = None


class ListThreadsResponse(msrest.serialization.Model):
    """ListThreadsResponse.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar threads: List of threads.
    :vartype threads: list[~azure.communication.chat.models.ThreadInfo]
    :ivar sync_state: Continuation link to get new and modified threads.
    :vartype sync_state: str
    :ivar backward_link: If there are more threads that can be retrieved, the backward link will be
     populated.
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

    def __init__(
        self,
        **kwargs
    ):
        super(ListThreadsResponse, self).__init__(**kwargs)
        self.threads = None
        self.sync_state = None
        self.backward_link = None


class Message(msrest.serialization.Model):
    """Message.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar id: The id of the message. This id is server generated.
    :vartype id: str
    :param message_type: Type of the message.
    
     Possible values:
    
     .. code-block::
    
        - Text
        - ThreadActivity/TopicUpdate
        - ThreadActivity/AddMember
        - ThreadActivity/DeleteMember.
    :type message_type: str
    :ivar client_message_id: The client message Id specified when the message was sent.
     This Id is a client-specific Id in a numeric unsigned Int64 format. It can be used for client
     deduping, among other client usages.
    :vartype client_message_id: str
    :param priority:  Possible values include: "Normal", "High".
    :type priority: str or ~azure.communication.chat.models.MessagePriority
    :ivar version: Version of the message.
    :vartype version: str
    :param content: Content of the message.
    :type content: str
    :param sender_display_name: The display name of the message sender. This property is used to
     populate sender name for push notifications.
    :type sender_display_name: str
    :ivar original_arrival_time: The timestamp when the message arrived at the server. The
     timestamp is in ISO8601 format: ``yyyy-MM-ddTHH:mm:ssZ``.
    :vartype original_arrival_time: ~datetime.datetime
    :ivar from_property: The Id of the message sender.
    :vartype from_property: str
    :param delete_time: The timestamp when the message was deleted in Unix time (epoch time) in
     milliseconds.
    :type delete_time: long
    :param edit_time: The timestamp when the message was edited in Unix time (epoch time) in
     milliseconds.
    :type edit_time: long
    """

    _validation = {
        'id': {'readonly': True},
        'client_message_id': {'readonly': True},
        'version': {'readonly': True},
        'original_arrival_time': {'readonly': True},
        'from_property': {'readonly': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'message_type': {'key': 'messageType', 'type': 'str'},
        'client_message_id': {'key': 'clientMessageId', 'type': 'str'},
        'priority': {'key': 'priority', 'type': 'str'},
        'version': {'key': 'version', 'type': 'str'},
        'content': {'key': 'content', 'type': 'str'},
        'sender_display_name': {'key': 'senderDisplayName', 'type': 'str'},
        'original_arrival_time': {'key': 'originalArrivalTime', 'type': 'iso-8601'},
        'from_property': {'key': 'from', 'type': 'str'},
        'delete_time': {'key': 'deleteTime', 'type': 'long'},
        'edit_time': {'key': 'editTime', 'type': 'long'},
    }

    def __init__(
        self,
        *,
        message_type: Optional[str] = None,
        priority: Optional[Union[str, "MessagePriority"]] = None,
        content: Optional[str] = None,
        sender_display_name: Optional[str] = None,
        delete_time: Optional[int] = None,
        edit_time: Optional[int] = None,
        **kwargs
    ):
        super(Message, self).__init__(**kwargs)
        self.id = None
        self.message_type = message_type
        self.client_message_id = None
        self.priority = priority
        self.version = None
        self.content = content
        self.sender_display_name = sender_display_name
        self.original_arrival_time = None
        self.from_property = None
        self.delete_time = delete_time
        self.edit_time = edit_time


class PostReadReceiptRequest(msrest.serialization.Model):
    """PostReadReceiptRequest.

    All required parameters must be populated in order to send to Azure.

    :param client_message_id: Required. The client message Id specified when the message was sent.
     This Id is a client-specific Id in a numeric unsigned Int64 format. It can be used for client
     deduping, among other client usages.
    :type client_message_id: str
    :param message_id: Required. Id of the latest message read by current user.
    :type message_id: str
    """

    _validation = {
        'client_message_id': {'required': True},
        'message_id': {'required': True},
    }

    _attribute_map = {
        'client_message_id': {'key': 'clientMessageId', 'type': 'str'},
        'message_id': {'key': 'messageId', 'type': 'str'},
    }

    def __init__(
        self,
        *,
        client_message_id: str,
        message_id: str,
        **kwargs
    ):
        super(PostReadReceiptRequest, self).__init__(**kwargs)
        self.client_message_id = client_message_id
        self.message_id = message_id


class ReadReceipt(msrest.serialization.Model):
    """ReadReceipt.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar user_id: Read receipt sender id.
    :vartype user_id: str
    :ivar message_id: Id for the message that has been read. This id is server generated.
    :vartype message_id: str
    :ivar read_timestamp: Read receipt timestamp.
    :vartype read_timestamp: long
    :ivar client_message_id: Client message id specified in the
     Microsoft.AzureCommunicationService.Gateway.Models.Client.CreateMessageRequest.
     This Id is a client-specific Id in a numeric unsigned Int64 format. It can be used for client
     deduping, among other client usages.
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

    def __init__(
        self,
        **kwargs
    ):
        super(ReadReceipt, self).__init__(**kwargs)
        self.user_id = None
        self.message_id = None
        self.read_timestamp = None
        self.client_message_id = None


class Thread(msrest.serialization.Model):
    """Thread.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar id: Thread id.
    :vartype id: str
    :param topic: Thread topic.
    :type topic: str
    :ivar created_at: Thread creation time in Unix time (epoch time) in milliseconds.
    :vartype created_at: str
    :ivar created_by: Id of the thread owner.
    :vartype created_by: str
    :param is_sticky_thread: Flag if a thread is sticky - sticky thread has an immutable member
     list, members cannot be added or removed.
    :type is_sticky_thread: bool
    :param members: Thread members.
    :type members: list[~azure.communication.chat.models.ThreadMember]
    """

    _validation = {
        'id': {'readonly': True},
        'created_at': {'readonly': True},
        'created_by': {'readonly': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'topic': {'key': 'topic', 'type': 'str'},
        'created_at': {'key': 'createdAt', 'type': 'str'},
        'created_by': {'key': 'createdBy', 'type': 'str'},
        'is_sticky_thread': {'key': 'isStickyThread', 'type': 'bool'},
        'members': {'key': 'members', 'type': '[ThreadMember]'},
    }

    def __init__(
        self,
        *,
        topic: Optional[str] = None,
        is_sticky_thread: Optional[bool] = None,
        members: Optional[List["ThreadMember"]] = None,
        **kwargs
    ):
        super(Thread, self).__init__(**kwargs)
        self.id = None
        self.topic = topic
        self.created_at = None
        self.created_by = None
        self.is_sticky_thread = is_sticky_thread
        self.members = members


class ThreadInfo(msrest.serialization.Model):
    """ThreadInfo.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar id: Thread id.
    :vartype id: str
    :param topic: Thread topic.
    :type topic: str
    :param is_deleted: Flag if a thread is soft deleted.
    :type is_deleted: bool
    :ivar last_message_received_time: The timestamp when the last message arrived at the server.
     The timestamp is in ISO8601 format: ``yyyy-MM-ddTHH:mm:ssZ``.
    :vartype last_message_received_time: ~datetime.datetime
    """

    _validation = {
        'id': {'readonly': True},
        'last_message_received_time': {'readonly': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'topic': {'key': 'topic', 'type': 'str'},
        'is_deleted': {'key': 'isDeleted', 'type': 'bool'},
        'last_message_received_time': {'key': 'lastMessageReceivedTime', 'type': 'iso-8601'},
    }

    def __init__(
        self,
        *,
        topic: Optional[str] = None,
        is_deleted: Optional[bool] = None,
        **kwargs
    ):
        super(ThreadInfo, self).__init__(**kwargs)
        self.id = None
        self.topic = topic
        self.is_deleted = is_deleted
        self.last_message_received_time = None


class ThreadMember(msrest.serialization.Model):
    """A member of the thread.

    All required parameters must be populated in order to send to Azure.

    :param id: Required. The id of the thread member in the format ``8:acs:ResourceId_AcsUserId``.
    :type id: str
    :param display_name: Display name for the thread member.
    :type display_name: str
    :param member_role: Required. Role of the thread member. The valid value should be "User" or
     "Admin". Possible values include: "Admin", "User".
    :type member_role: str or ~azure.communication.chat.models.MemberRole
    :param share_history_time: Time from which the group chat history is shared with the member in
     EPOCH time (milliseconds).
    
     Possible values:
    
    
     * ``0`` which means share everything
     * ``-1`` which means share nothing
     * ``1594691284031`` which is epoch time equivalent to 7/14/2020 1:48:04 AM +00:00.
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

    def __init__(
        self,
        *,
        id: str,
        member_role: Union[str, "MemberRole"],
        display_name: Optional[str] = None,
        share_history_time: Optional[str] = None,
        **kwargs
    ):
        super(ThreadMember, self).__init__(**kwargs)
        self.id = id
        self.display_name = display_name
        self.member_role = member_role
        self.share_history_time = share_history_time


class UpdateMessageRequest(msrest.serialization.Model):
    """UpdateMessageRequest.

    :param content: Chat message content.
    :type content: str
    """

    _attribute_map = {
        'content': {'key': 'content', 'type': 'str'},
    }

    def __init__(
        self,
        *,
        content: Optional[str] = None,
        **kwargs
    ):
        super(UpdateMessageRequest, self).__init__(**kwargs)
        self.content = content


class UpdateThreadRequest(msrest.serialization.Model):
    """UpdateThreadRequest.

    :param topic: Thread topic.
    :type topic: str
    """

    _attribute_map = {
        'topic': {'key': 'topic', 'type': 'str'},
    }

    def __init__(
        self,
        *,
        topic: Optional[str] = None,
        **kwargs
    ):
        super(UpdateThreadRequest, self).__init__(**kwargs)
        self.topic = topic
