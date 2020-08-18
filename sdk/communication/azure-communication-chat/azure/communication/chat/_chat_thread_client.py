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

from ._common import CommunicationUserCredential, CommunicationUserCredentialPolicy
from ._generated import AzureCommunicationChatService
from ._generated.models import (
    AddChatThreadMembersRequest,
    PostReadReceiptRequest,
    SendChatMessageRequest,
    UpdateChatMessageRequest,
    UpdateChatThreadRequest
)
from ._utils import _to_utc_datetime # pylint: disable=unused-import

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar, Union
    from datetime import datetime


class ChatThreadClient(object):
    """A client to interact with the AzureCommunicationService Chat gateway.
    Instances of this class is normally created by ChatClient.create_thread()

    This client provides operations to add member to chat thread, remove member from
    chat thread, send message, delete message, update message, send typing notifications,
    send and list read receipt

    :param str thread_id:
        The unique thread id.
    :param str endpoint:
        The endpoint of the Azure Communication resource.
    :param str credential:
        The credentials with which to authenticate. The value is an User
        Access Token
    """
    def __init__(
            self,
            thread_id,  # type: str
            endpoint,  # type: str
            credential,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        if not thread_id:
            raise ValueError("thread_id can not be None or empty")

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

        self._thread_id = thread_id
        self._endpoint = endpoint
        self._credential = credential

        self._client = AzureCommunicationChatService(
            endpoint,
            authentication_policy=CommunicationUserCredentialPolicy(CommunicationUserCredential(credential)),
            **kwargs
        )

    @property
    def thread_id(self):
        # type: () -> str
        """
        Gets the thread id from the client.

        :rtype: str
        """
        return self._thread_id

    @distributed_trace
    def update_thread(
            self,
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Updates a thread's properties.

        :keyword str topic: Thread topic.
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        topic = kwargs.pop("topic", None)

        update_thread_request = UpdateChatThreadRequest(topic=topic)
        return self._client.update_chat_thread(
            chat_thread_id=self._thread_id,
            body=update_thread_request,
            **kwargs)

    @distributed_trace
    def send_read_receipt(
            self,
            message_id,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Posts a read receipt event to a thread, on behalf of a user.

        :param message_id: Required. Id of the latest message read by current user.
        :type message_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not message_id:
            raise ValueError("post_read_receipt_request cannot be None.")

        post_read_receipt_request = PostReadReceiptRequest(chat_message_id=message_id)
        return self._client.send_chat_read_receipt(
            self._thread_id,
            body=post_read_receipt_request,
            **kwargs)

    @distributed_trace
    def list_read_receipts(
            self,
            **kwargs  # type: Any
    ):
        # type: (...) -> list[ReadReceipt]
        """Gets read receipts for a thread.

        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: list of ReadReceipt, or the result of cls(response)
        :rtype: list[~azure.communication.chat.models.ReadReceipt]
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        return self._client.list_chat_read_receipts(self._thread_id, **kwargs)

    @distributed_trace
    def send_typing_notification(
            self,
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Posts a typing event to a thread, on behalf of a user.

        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        return self._client.send_typing_notification(self._thread_id, **kwargs)

    @distributed_trace
    def send_message(
            self,
            content,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> SendMessageResult
        """Sends a message to a thread.

        :param content: Required. Chat message content.
        :type content: str
        :keyword ChatMessagePriorityDto priority: Message priority.
        :keyword str sender_display_name: The display name of the message sender. This property is used to
          populate sender name for push notifications.
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: SendMessageResult, or the result of cls(response)
        :rtype: ~azure.communication.chat.models.SendMessageResult
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not content:
            raise ValueError("content cannot be None.")

        priority = kwargs.pop("priority", None)
        sender_display_name = kwargs.pop("sender_display_name", None)

        create_message_request = SendChatMessageRequest(
            content=content,
            priority=priority,
            sender_display_name=sender_display_name
        )
        return self._client.send_chat_message(
            chat_thread_id=self._thread_id,
            body=create_message_request,
            **kwargs)

    @distributed_trace
    def get_message(
            self,
            message_id,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> ChatMessage
        """Gets a message by id.

        :param message_id: Required. The message id.
        :type message_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: ChatMessage, or the result of cls(response)
        :rtype: ~azure.communication.chat.models.ChatMessage
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not message_id:
            raise ValueError("message_id cannot be None.")

        return self._client.get_chat_message(
            self._thread_id,
            message_id,
            **kwargs)

    @distributed_trace
    def list_messages(
            self,
            **kwargs  # type: Any
    ):
        # type: (...) -> ListChatMessagesResult
        """Gets a list of messages from a thread.

        :keyword int page_size: The number of messages being requested.
        :keyword ~datetime.datetime start_time: The start time(UTC) where the range query.
        :keyword str sync_state: The continuation token that previous request obtained. This is
         used for paging.
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: ListChatMessagesResult, or the result of cls(response)
        :rtype: ~azure.communication.chat.models.ListChatMessagesResult
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        page_size = kwargs.pop("page_size", None)
        start_time = kwargs.pop("start_time", None)
        sync_state = kwargs.pop("sync_state", None)

        return self._client.list_chat_messages(
            self._thread_id,
            page_size=page_size,
            start_time=start_time,
            sync_state=sync_state,
            **kwargs)

    @distributed_trace
    def update_message(
            self,
            message_id,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Updates a message.

        :param message_id: Required. The message id.
        :type message_id: str
        :keyword str content: Chat message content.
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not message_id:
            raise ValueError("message_id cannot be None.")

        content = kwargs.pop("content", None)

        update_message_request = UpdateChatMessageRequest(content=content)

        return self._client.update_chat_message(
            chat_thread_id=self._thread_id,
            chat_message_id=message_id,
            body=update_message_request,
            **kwargs)

    @distributed_trace
    def delete_message(
            self,
            message_id,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Deletes a message.

        :param message_id: Required. The message id.
        :type message_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not message_id:
            raise ValueError("message_id cannot be None.")

        return self._client.delete_chat_message(
            chat_thread_id=self._thread_id,
            chat_message_id=message_id,
            **kwargs)

    @distributed_trace
    def list_members(
            self,
            **kwargs  # type: Any
    ):
        # type: (...) -> list[ChatThreadMember]
        """Gets the members of a thread.

        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: list of ChatThreadMember, or the result of cls(response)
        :rtype: list[~azure.communication.chat.models.ChatThreadMember]
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        return self._client.list_chat_thread_members(self._thread_id, **kwargs)

    @distributed_trace
    def add_members(
            self,
            thread_members,  # type: list[ChatThreadMember]
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Adds thread members to a thread. If members already exist, no change occurs.

        :param thread_members: Required. Thread members to be added to the thread.
        :type thread_members: list[~azure.communication.chat.models.ChatThreadMember]
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_members:
            raise ValueError("thread_members cannot be None.")

        add_thread_members_request = AddChatThreadMembersRequest(members=thread_members)

        return self._client.add_chat_thread_members(
            chat_thread_id=self._thread_id,
            body=add_thread_members_request,
            **kwargs)

    @distributed_trace
    def remove_member(
            self,
            member_id,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Remove a member from a thread.

        :param member_id: Required. Id of the thread member to remove from the thread.
        :type member_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not member_id:
            raise ValueError("member_id cannot be None.")

        return self._client.remove_chat_thread_member(
            chat_thread_id=self._thread_id,
            chat_member_id=member_id,
            **kwargs)

    def close(self):
        # type: () -> None
        return self._client.close()

    def __enter__(self):
        # type: () -> ChatThreadClient
        self._client.__enter__()  # pylint:disable=no-member
        return self

    def __exit__(self, *args):
        # type: (*Any) -> None
        self._client.__exit__(*args)  # pylint:disable=no-member
