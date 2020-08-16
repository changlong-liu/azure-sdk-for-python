# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
from typing import TYPE_CHECKING

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse # type: ignore

import six
from azure.core.tracing.decorator import distributed_trace

from ._generated import AzureCommunicationChatService
from ._generated.models import (
    AddThreadMembersRequest,
    CreateThreadRequest,
    SendMessageRequest,
    MessagePriority,
    PostReadReceiptRequest,
    UpdateMessageRequest,
    UpdateThreadRequest
)
from ._common import CommunicationUserCredential, CommunicationUserCredentialPolicy

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar, Union

POLLING_INTERVAL = 5


class ChatClient(object):
    """A client to interact with the AzureCommunicationService Chat gateway.

    This client provides operations to create a chat thread, delete a thread,
    get thread by id, get threads, add member to thread, remove member from
    thread, send message, delete message, update message.

    :param str credential:
        The credentials with which to authenticate. The value is an User
        Access Token
    :param str endpoint:
        The endpoint of the Azure Communication resource.
    :keyword int polling_interval:
        Default waiting time between two polls for LRO operations if no
        Retry-After header is present.
    """
    def __init__(
            self,
            credential,  # type: str
            endpoint,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        if not credential:
            raise ValueError("credential can not be None or empty")
        if not isinstance(credential, six.string_types):
            raise TypeError("credential must be a string.")

        try:
            if not endpoint.lower().startswith('http'):
                endpoint = "https://" + endpoint
        except AttributeError:
            raise ValueError("Host URL must be a string")

        parsed_url = urlparse(endpoint.rstrip('/'))
        if not parsed_url.netloc:
            raise ValueError("Invalid URL: {}".format(endpoint))

        self._credential = CommunicationUserCredential(credential)
        self._polling_interval = kwargs.pop("polling_interval", POLLING_INTERVAL)

        self._client = AzureCommunicationChatService(
            endpoint,
            polling_interval=self._polling_interval,
            authentication_policy=CommunicationUserCredentialPolicy(self._credential),
            **kwargs
        )

    @distributed_trace
    def create_chat_thread(
            self, topic,  # type: str
            thread_members,  # type: list[ThreadMember]
            **kwargs  # type: Any
    ):
        # type: (...) -> CreateThreadResult
        """Creates a chat thread.

        :param topic: Required. The thread topic.
        :type topic: str
        :param thread_members: Required. Members to be added to the thread.
        :type thread_members: list[~azure.communication.chat.models.ThreadMember]
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: CreateThreadResponse, or the result of cls(response)
        :rtype: ~azure.communication.chat.models.CreateThreadResult
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not topic:
            raise ValueError("topic cannot be None.")
        if not thread_members:
            raise ValueError("List of ThreadMember cannot be None.")

        create_thread_request = CreateThreadRequest(topic=topic, members=thread_members)

        return self._client.create_thread(create_thread_request, **kwargs)

    @distributed_trace
    def get_chat_thread(
            self, thread_id,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> Thread
        """Gets a chat thread.

        :param thread_id: Required. Thread id to get.
        :type thread_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Thread, or the result of cls(response)
        :rtype: ~azure.communication.chat.models.Thread
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")

        return self._client.get_thread(thread_id, **kwargs)

    @distributed_trace
    def list_chat_threads(
        self,
        **kwargs
    ):
        # type: (...) -> ListThreadsResult
        """Gets the list of chat threads of a user.

        :keyword int page_size: The number of threads being requested.
        :keyword long start_time: The start time where the range query. This is represented by number of
         seconds since epoch time.
        :keyword str sync_state: The continuation token that previous request obtained. This is used for
         paging.
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: ListThreadsResult, or the result of cls(response)
        :rtype: ~azure.communication.chat.models.ListThreadsResult
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        page_size = kwargs.pop("page_size", None)
        start_time = kwargs.pop("start_time", None)
        sync_state = kwargs.pop("sync_state", None)

        return self._client.list_threads(
            page_size=page_size,
            start_time=start_time,
            sync_state=sync_state,
            **kwargs)

    @distributed_trace
    def update_chat_thread(
            self,
            thread_id,  # type: str
            topic,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Updates a thread's properties.

        :param thread_id: Required. The id of the thread to update.
        :type thread_id: str
        :param topic: Required. Thread topic.
        :type topic: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")
        if not topic:
            raise ValueError("topic cannot be None")

        update_thread_request = UpdateThreadRequest(topic=topic)
        return self._client.update_thread(
            thread_id=thread_id,
            body=update_thread_request,
            **kwargs)

    @distributed_trace
    def delete_chat_thread(
            self,
            thread_id,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Deletes a thread.

        :param thread_id: Required. Thread id to delete.
        :type thread_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")

        return self._client.delete_thread(thread_id, **kwargs)

    @distributed_trace
    def send_chat_message(
            self,
            thread_id,  # type: str
            content,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> CreateMessageResult
        """Sends a message to a thread.

        :param thread_id: Required. The thread id to send the message to.
        :type thread_id: str
        :param content: Required. Chat message content.
        :type content: str
        :keyword Union[str,MessagePriority] priority: Message priority.
        :keyword str sender_display_name: The display name of the message sender. This property is used to
          populate sender name for push notifications.
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: CreateMessageResult, or the result of cls(response)
        :rtype: ~azure.communication.chat.models.CreateMessageResult
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")
        if not content:
            raise ValueError("content cannot be None.")

        priority = kwargs.pop("priority", None)
        sender_display_name = kwargs.pop("sender_display_name", None)

        create_message_request=SendMessageRequest(
            content=content,
            priority=priority,
            sender_display_name=sender_display_name
        )
        return self._client.send_message(
            thread_id=thread_id,
            body=create_message_request,
            **kwargs)

    @distributed_trace
    def get_chat_message(
            self,
            thread_id,  # type: str
            message_id,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> Message
        """Gets a message by id.

        :param thread_id: Required. The thread id to which the message was sent.
        :type thread_id: str
        :param message_id: Required. The message id.
        :type message_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Message, or the result of cls(response)
        :rtype: ~azure.communication.chat.models.Message
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")
        if not message_id:
            raise ValueError("message_id cannot be None.")

        return self._client.get_message(
            thread_id,
            message_id,
            **kwargs)

    @distributed_trace
    def list_chat_messages(
            self,
            thread_id,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> ListMessagesResult
        """Gets a list of messages from a thread.

        :param thread_id: Required. The thread id of the message.
        :type thread_id: str
        :keyword int page_size: The number of messages being requested.
        :keyword long start_time: The start time where the range query. This is represented
         by number of seconds since epoch time.
        :keyword str sync_state: The continuation token that previous request obtained. This is
         used for paging.
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: ListMessagesResult, or the result of cls(response)
        :rtype: ~azure.communication.chat.models.ListMessagesResult
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")

        page_size = kwargs.pop("page_size", None)
        start_time = kwargs.pop("start_time", None)
        sync_state = kwargs.pop("sync_state", None)

        return self._client.list_messages(
            thread_id,
            page_size=page_size,
            start_time=start_time,
            sync_state=sync_state,
            **kwargs)

    @distributed_trace
    def update_chat_message(
            self,
            thread_id,  # type: str
            message_id,  # type: str
            content,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Updates a message.

        :param thread_id: Required. The thread id to which the message was sent.
        :type thread_id: str
        :param message_id: Required. The message id.
        :type message_id: str
        :param content: Chat message content.
        :type content: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")
        if not message_id:
            raise ValueError("message_id cannot be None.")
        if not content:
            raise ValueError("content cannot be None.")

        update_message_request = UpdateMessageRequest(content=content)

        return self._client.update_message(
            thread_id=thread_id,
            message_id=message_id,
            body=update_message_request,
            **kwargs)

    @distributed_trace
    def delete_chat_message(
            self,
            thread_id,  # type: str
            message_id,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Deletes a message.

        :param thread_id: Required. The thread id to which the message was sent.
        :type thread_id: str
        :param message_id: Required. The message id.
        :type message_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")
        if not message_id:
            raise ValueError("message_id cannot be None.")

        return self._client.delete_message(
            thread_id=thread_id,
            message_id=message_id,
            **kwargs)

    @distributed_trace
    def list_chat_members(
            self,
            thread_id,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> list[ThreadMember]
        """Gets the members of a thread.

        :param thread_id: Required. Thread id to get members for.
        :type thread_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: list of ThreadMember, or the result of cls(response)
        :rtype: list[~azure.communication.chat.models.ThreadMember]
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")

        return self._client.list_thread_members(thread_id, **kwargs)

    @distributed_trace
    def add_chat_members(
            self,
            thread_id,  # type: str
            thread_members,  # type: list[ThreadMember]
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Adds thread members to a thread. If members already exist, no change occurs.

        :param thread_id: Required. Id of the thread to add members to.
        :type thread_id: str
        :param thread_members: Required. Thread members to be added to the thread.
        :type thread_members: list[~azure.communication.chat.models.ThreadMember]
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")
        if not thread_members:
            raise ValueError("thread_members cannot be None.")

        add_thread_members_request = AddThreadMembersRequest(members=thread_members)

        return self._client.add_thread_members(
            thread_id=thread_id,
            body=add_thread_members_request,
            **kwargs)

    @distributed_trace
    def remove_chat_member(
            self,
            thread_id,  # type: str
            member_id,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Remove a member from a thread.

        :param thread_id: Required. Thread id to remove the member from.
        :type thread_id: str
        :param member_id: Required. Id of the thread member to remove from the thread.
        :type member_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")
        if not member_id:
            raise ValueError("member_id cannot be None.")

        return self._client.remove_thread_member(
            thread_id=thread_id,
            member_id=member_id,
            **kwargs)

    @distributed_trace
    def send_typing_notification(
            self,
            thread_id,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Posts a typing event to a thread, on behalf of a user.

        :param thread_id: Required. Id of the thread.
        :type thread_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")

        return self._client.notify_user_typing(thread_id, **kwargs)

    @distributed_trace
    def send_read_receipt(
            self,
            thread_id,  # type: str
            message_id,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Posts a read receipt event to a thread, on behalf of a user.

        :param thread_id: Required. Id of the thread.
        :type thread_id: str
        :param message_id: Required. Id of the latest message read by current user.
        :type message_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")
        if not message_id:
            raise ValueError("post_read_receipt_request cannot be None.")

        post_read_receipt_request = PostReadReceiptRequest(message_id=message_id)
        return self._client.send_read_receipt(
            thread_id,
            body=post_read_receipt_request,
            **kwargs)

    @distributed_trace
    def list_read_receipts(
            self,
            thread_id,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> list[ReadReceipt]
        """Gets read receipts for a thread.

        :param thread_id: Required. Thread id to get the read receipts for.
        :type thread_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: list of ReadReceipt, or the result of cls(response)
        :rtype: list[~azure.communication.chat.models.ReadReceipt]
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")

        return self._client.list_read_receipts(thread_id, **kwargs)

    def close(self):
        # type: () -> None
        return self._client.close()

    def __enter__(self):
        # type: () -> ChatClient
        self._client.__enter__()  # pylint:disable=no-member
        return self

    def __exit__(self, *args):
        # type: (*Any) -> None
        self._client.__exit__(*args)  # pylint:disable=no-member
