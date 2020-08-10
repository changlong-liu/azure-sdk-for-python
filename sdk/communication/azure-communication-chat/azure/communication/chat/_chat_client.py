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

from ._generated import models # pylint: disable=unused-import
from ._generated import AzureCommunicationChatService
from ._common import CommunicationUserCredential, CommunicationUserCredentialPolicy

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar

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
    def create_thread(
            self, create_thread_request,  # type: models.CreateThreadRequest
            correlation_vector=None,  # type: Optional[str]
            **kwargs  # type: Any
    ):
        # type: (...) -> models.CreateThreadResponse
        """Creates a chat thread.

        :param create_thread_request: Request payload for creating a chat thread.
        :type create_thread_request: ~azure.communication.chat.models.CreateThreadRequest
        :param correlation_vector: Correlation vector, if a value is not
            provided a randomly generated correlation vector would be returned
            in the response header "MS-CV".
        :type correlation_vector: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: CreateThreadResponse, or the result of cls(response)
        :rtype: models.CreateThreadResponse
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not create_thread_request:
            raise ValueError("create_thread_request cannot be None.")

        return self._client.create_thread(correlation_vector, create_thread_request, **kwargs)

    @distributed_trace
    def get_thread(
            self, thread_id,  # type: str
            correlation_vector=None,  # type: Optional[str]
            **kwargs  # type: Any
    ):
        # type: (...) -> models.Thread
        """Gets a chat thread.

        :param thread_id: Thread id to get.
        :type thread_id: str
        :param correlation_vector: Correlation vector, if a value is not
         provided a randomly generated correlation vector would be returned
         in the response header "MS-CV".
        :type correlation_vector: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Thread, or the result of cls(response)
        :rtype: models.Thread
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")

        return self._client.get_thread(thread_id, correlation_vector, **kwargs)

    @distributed_trace
    def update_thread(
            self,
            thread_id,  # type: str
            update_thread_request,  # type: models.UpdateThreadRequest
            correlation_vector=None,  # type: Optional[str]
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Updates a thread's properties.

        :param thread_id: The id of the thread to update.
        :type thread_id: str
        :param update_thread_request: Request payload for updating a chat thread.
        :type update_thread_request: ~azure.communication.chat.models.UpdateThreadRequest
        :param correlation_vector: Correlation vector, if a value is not
         provided a randomly generated correlation vector would be returned
         in the response header "MS-CV".
        :type correlation_vector: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")
        if not update_thread_request:
            raise ValueError("update_thread_request cannot be None")

        return self._client.update_thread(
            thread_id=thread_id,
            correlation_vector=correlation_vector,
            body=update_thread_request,
            **kwargs)

    @distributed_trace
    def delete_thread(
            self,
            thread_id,  # type: str
            correlation_vector=None,  # type: Optional[str]
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Deletes a thread.

        :param thread_id: Thread id to delete.
        :type thread_id: str
        :param correlation_vector: Correlation vector, if a value is not
         provided a randomly generated correlation vector would be returned
         in the response header "MS-CV".
        :type correlation_vector: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")

        return self._client.delete_thread(thread_id, correlation_vector, **kwargs)

    @distributed_trace
    def send_message(
            self,
            thread_id,  # type: str
            create_message_request,  # type: models.CreateMessageRequest
            correlation_vector=None,  # type: Optional[str]
            **kwargs  # type: Any
    ):
        # type: (...) -> models.CreateMessageResponse
        """Sends a message to a thread.

        :param thread_id: The thread id to send the message to.
        :type thread_id: str
        :param create_message_request: Details of the message to create.
        :type create_message_request: ~azure.communication.chat.models.CreateMessageRequest
        :param correlation_vector: Correlation vector, if a value is not
         provided a randomly generated correlation vector would be returned
         in the response header "MS-CV".
        :type correlation_vector: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: CreateMessageResponse, or the result of cls(response)
        :rtype: models.CreateMessageResponse
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")
        if not create_message_request:
            raise ValueError("create_message_request cannot be None.")

        return self._client.send_message(
            thread_id=thread_id,
            correlation_vector=correlation_vector,
            body=create_message_request,
            **kwargs)

    @distributed_trace
    def get_message(
            self,
            thread_id,  # type: str
            message_id,  # type: str
            correlation_vector=None,  # type: Optional[str]
            **kwargs  # type: Any
    ):
        # type: (...) -> models.Message
        """Gets a message by id.

        :param thread_id: The thread id to which the message was sent.
        :type thread_id: str
        :param message_id: The message id.
        :type message_id: str
        :param correlation_vector: Correlation vector, if a value is not
         provided a randomly generated correlation vector would be returned
         in the response header "MS-CV".
        :type correlation_vector: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Message, or the result of cls(response)
        :rtype: models.Message
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")
        if not message_id:
            raise ValueError("message_id cannot be None.")

        return self._client.get_message(
            thread_id,
            message_id,
            correlation_vector=correlation_vector,
            **kwargs)

    @distributed_trace
    def list_messages(
            self,
            thread_id,  # type: str
            correlation_vector=None,  # type: Optional[str]
            **kwargs  # type: Any
    ):
        # type: (...) -> models.ListMessagesResponse
        """Gets a list of messages from a thread.

        :param thread_id: The thread id of the message.
        :type thread_id: str
        :param page_size: The number of messages being requested.
        :type page_size: int
        :param start_time: The start time where the range query. This is represented by number of
         seconds since epoch time.
        :type start_time: long
        :param sync_state: The continuation token that previous request obtained. This is used for
         paging.
        :type sync_state: str
        :param correlation_vector: Correlation vector, if a value is not
         provided a randomly generated correlation vector would be returned
         in the response header "MS-CV".
        :type correlation_vector: str
        :keyword int page_size: The number of messages being requested.
        :keyword long start_time: The start time where the range query. This is represented
         by number of seconds since epoch time.
        :keyword str sync_state: The continuation token that previous request obtained. This is
         used for paging.
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: ListMessagesResponse, or the result of cls(response)
        :rtype: models.ListMessagesResponse
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
            correlation_vector=correlation_vector,
            **kwargs)

    @distributed_trace
    def update_message(
            self,
            thread_id,  # type: str
            message_id,  # type: str
            update_message_request,  # type: models.UpdateMessageRequest
            correlation_vector=None,  # type: Optional[str]
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Updates a message.

        :param thread_id: The thread id to which the message was sent.
        :type thread_id: str
        :param message_id: The message id.
        :type message_id: str
        :param update_message_request: Details of the request to update the message.
        :type update_message_request: ~azure.communication.chat.models.UpdateMessageRequest
        :param correlation_vector: Correlation vector, if a value is not
         provided a randomly generated correlation vector would be returned
         in the response header "MS-CV".
        :type correlation_vector: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")
        if not message_id:
            raise ValueError("message_id cannnot be None.")
        if not update_message_request:
            raise ValueError("update_message_request cannot be None.")

        return self._client.update_message(
            thread_id=thread_id,
            message_id=message_id,
            correlation_vector=correlation_vector,
            body=update_message_request,
            **kwargs)

    @distributed_trace
    def delete_message(
            self,
            thread_id,  # type: str
            message_id,  # type: str
            correlation_vector=None,  # type: Optional[str]
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Deletes a message.

        :param thread_id: The thread id to which the message was sent.
        :type thread_id: str
        :param message_id: The message id.
        :type message_id: str
        :param correlation_vector: Correlation vector, if a value is not
         provided a randomly generated correlation vector would be returned
         in the response header "MS-CV".
        :type correlation_vector: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")
        if not message_id:
            raise ValueError("message_id cannnot be None.")

        return self._client.delete_message(
            thread_id=thread_id,
            message_id=message_id,
            correlation_vector=correlation_vector,
            **kwargs)

    @distributed_trace
    def list_members(
            self,
            thread_id,  # type: str
            correlation_vector=None,  # type: Optional[str]
            **kwargs  # type: Any
    ):
        # type: (...) -> [models.ThreadMember]
        """Gets the members of a thread.

        :param thread_id: Thread id to get members for.
        :type thread_id: str
        :param correlation_vector: Correlation vector, if a value is not
         provided a randomly generated correlation vector would be returned
         in the response header "MS-CV".
        :type correlation_vector: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: list of ThreadMember, or the result of cls(response)
        :rtype: [models.ThreadMember]
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")

        return self._client.list_thread_members(thread_id, correlation_vector, **kwargs)

    @distributed_trace
    def add_members(
            self,
            thread_id,  # type: str
            add_thread_members_request,  # type: models.AddThreadMembersRequest
            correlation_vector=None,  # type: Optional[str]
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Adds thread members to a thread. If members already exist, no change occurs.

        :param thread_id: Id of the thread to add members to.
        :type thread_id: str
        :param add_thread_members_request: Thread members to be added to the thread.
        :type add_thread_members_request: ~azure.communication.chat.models.AddThreadMembersRequest
        :param correlation_vector: Correlation vector, if a value is not
         provided a randomly generated correlation vector would be returned
         in the response header "MS-CV".
        :type correlation_vector: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")
        if not add_thread_members_request:
            raise ValueError("add_thread_members_request cannnot be None.")

        return self._client.add_thread_members(
            thread_id=thread_id,
            correlation_vector=correlation_vector,
            body=add_thread_members_request,
            **kwargs)

    @distributed_trace
    def remove_member(
            self,
            thread_id,  # type: str
            member_id,  # type: str
            correlation_vector=None,  # type: Optional[str]
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Remove a member from a thread.

        :param thread_id: Thread id to remove the member from.
        :type thread_id: str
        :param member_id: Id of the thread member to remove from the thread.
        :type member_id: str
        :param correlation_vector: Correlation vector, if a value is not
         provided a randomly generated correlation vector would be returned
         in the response header "MS-CV".
        :type correlation_vector: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")
        if not member_id:
            raise ValueError("member_id cannnot be None.")

        return self._client.remove_thread_member(
            thread_id=thread_id,
            member_id=member_id,
            correlation_vector=correlation_vector,
            **kwargs)

    @distributed_trace
    def send_typing_notification(
            self,
            thread_id,  # type: str
            correlation_vector=None,  # type: Optional[str]
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Posts a typing event to a thread, on behalf of a user.

        :param thread_id: Id of the thread.
        :type thread_id: str
        :param correlation_vector: Correlation vector, if a value is not provided a randomly generated
         correlation vector would be returned in the response header "MS-CV".
        :type correlation_vector: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")

        return self._client.notify_user_typing(thread_id, correlation_vector, **kwargs)

    @distributed_trace
    def send_read_receipt(
            self,
            thread_id,  # type: str
            post_read_receipt_request,  # type: models.PostReadReceiptRequest
            correlation_vector=None,  # type: Optional[str]
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Posts a read receipt event to a thread, on behalf of a user.

        :param thread_id: Id of the thread.
        :type thread_id: str
        :param post_read_receipt_request: Request payload for sending a read receipt.
        :type post_read_receipt_request: ~azure.communication.chat.models.PostReadReceiptRequest
        :param correlation_vector: Correlation vector, if a value is not provided a randomly generated
         correlation vector would be returned in the response header "MS-CV".
        :type correlation_vector: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")
        if not post_read_receipt_request:
            raise ValueError("post_read_receipt_request cannnot be None.")

        return self._client.send_read_receipt(
            thread_id,
            correlation_vector=correlation_vector,
            body=post_read_receipt_request,
            **kwargs)

    @distributed_trace
    def list_read_receipts(
            self,
            thread_id,  # type: str
            correlation_vector=None,  # type: Optional[str]
            **kwargs  # type: Any
    ):
        # type: (...) -> List["models.ReadReceipt"]
        """Gets read receipts for a thread.

        :param thread_id: Thread id to get the read receipts for.
        :type thread_id: str
        :param correlation_vector: Correlation vector, if a value is not provided a randomly generated
         correlation vector would be returned in the response header "MS-CV".
        :type correlation_vector: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: list of ReadReceipt, or the result of cls(response)
        :rtype: list[~azure.communication.chat.models.ReadReceipt]
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")

        return self._client.list_read_receipts(thread_id, correlation_vector, **kwargs)

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
