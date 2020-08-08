# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import six
from urllib.parse import urlparse
from azure.core.tracing.decorator import distributed_trace

from ._generated import models
from ._generated import AzureCommunicationChatService
from ._common import CommunicationUserCredential, CommunicationUserCredentialPolicy

POLLING_INTERVAL = 5


class ChatClient(object):
    """A client to interact with the AzureCommunicationService Chat gateway.

    This client provides operations to create a chat thread, delete a thread,
    get thread by id, get threads, add member to thread, remove member from
    thread, send message, delete message, update message.

    :param token: A token to authorize chat client requests
    :type token: str
    :param endpoint: The endpoint of the Azure Communication resource.
    :type endpoint: str
    :keyword int polling_interval: Default waiting time between two polls for LRO operations if no Retry-After header is present.
    """

    def __init__(
            self, 
            token,  # type: str
            endpoint,  # type: str
            **kwargs  # type: Any
    ):
        if not token:
            raise ValueError("token can not be None or empty")
        if not isinstance(token, six.string_types):
            raise TypeError("token must be a string.")

        try:
            if not endpoint.lower().startswith('http'):
                endpoint = "https://" + endpoint
        except AttributeError:
            raise ValueError("Host URL must be a string")

        parsed_url = urlparse(endpoint.rstrip('/'))
        if not parsed_url.netloc:
            raise ValueError("Invalid URL: {}".format(endpoint))

        self._credential = CommunicationUserCredential(token)
        self._polling_interval = kwargs.pop("polling_interval", POLLING_INTERVAL)

        self._client = AzureCommunicationChatService(
            endpoint,
            polling_interval=self._polling_interval,
            authentication_policy=CommunicationUserCredentialPolicy(self._credential),
            **kwargs
        )

    @distributed_trace
    def create_thread(
        self,
        create_thread_request,  # type: "models.CreateThreadRequest"
        correlation_vector=None,  # type: Optional[str]
        **kwargs  # type: **Any -> Dict[str, str]
    ):
        # type: (...) -> "models.CreateThreadResponse"
        """Creates a chat thread.

        Creates a chat thread.

        :param create_thread_request: Request payload for creating a chat thread.
        :type create_thread_request: ~azure.communication.chat.models.CreateThreadRequest
        :param correlation_vector: Correlation vector, if a value is not provided a randomly generated
         correlation vector would be returned in the response header "MS-CV".
        :type correlation_vector: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: CreateThreadResponse, or the result of cls(response)
        :rtype: ~azure.communication.chat.models.CreateThreadResponse
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not create_thread_request:
            raise ValueError("create_thread_request cannot be None.")

        return self._client.create_thread(correlation_vector, create_thread_request, **kwargs)

    @distributed_trace
    def get_thread(
        self,
        thread_id,  # type: str
        correlation_vector=None,  # type: Optional[str]
        **kwargs  # type: Any
    ):
        """Gets a chat thread.

        Gets a chat thread.

        :param thread_id: Thread id to get.
        :type thread_id: str
        :param correlation_vector: Correlation vector, if a value is not provided a randomly generated
         correlation vector would be returned in the response header "MS-CV".
        :type correlation_vector: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Thread, or the result of cls(response)
        :rtype: ~azure.communication.chat.models.Thread
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        # type: (...) -> "models.Thread"
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

        Updates a thread's properties.

        :param thread_id: The id of the thread to update.
        :type thread_id: str
        :param update_thread_request: Request payload for updating a chat thread.
        :type update_thread_request: ~azure.communication.chat.models.UpdateThreadRequest
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
        if not update_thread_request:
            raise ValueError("update_thread_request cannot be None")

        return self._client.update_thread(thread_id, correlation_vector, update_thread_request, **kwargs)

    @distributed_trace
    def delete_thread(
        self,
        thread_id,  # type: str
        correlation_vector=None,  # type: Optional[str]
        **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Deletes a thread.

        Deletes a thread.

        :param thread_id: Thread id to delete.
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

        return self._client.delete_thread(thread_id, correlation_vector, **kwargs)

    @distributed_trace
    def send_message(
        self,
        thread_id,  # type: str
        create_message_request,  # type: models.CreateMessageRequest
        correlation_vector=None,  # type: Optional[str]
        **kwargs  # type: Any
    ):
        # type: (...) -> "models.CreateMessageResponse"
        """Sends a message to a thread.

        Sends a message to a thread.

        :param thread_id: The thread id to send the message to.
        :type thread_id: str
        :param create_message_request: Details of the message to create.
        :type create_message_request: ~azure.communication.chat.models.CreateMessageRequest
        :param correlation_vector: Correlation vector, if a value is not provided a randomly generated
         correlation vector would be returned in the response header "MS-CV".
        :type correlation_vector: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: CreateMessageResponse, or the result of cls(response)
        :rtype: ~azure.communication.chat.models.CreateMessageResponse
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")
        if not create_message_request:
            raise ValueError("create_message_request cannot be None.")

        return self._client.send_message(thread_id, correlation_vector, create_message_request, **kwargs)

    @distributed_trace
    def get_message(
        self,
        thread_id,  # type: str
        message_id,  # type: str
        correlation_vector=None,  # type: Optional[str]
        **kwargs  # type: Any
    ):
        # type: (...) -> "models.Message"
        """Gets a message by id.

        Gets a message by id.

        :param thread_id: The thread id to which the message was sent.
        :type thread_id: str
        :param message_id: The message id.
        :type message_id: str
        :param correlation_vector: Correlation vector, if a value is not provided a randomly generated
         correlation vector would be returned in the response header "MS-CV".
        :type correlation_vector: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Message, or the result of cls(response)
        :rtype: ~azure.communication.chat.models.Message
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")
        if not message_id:
            raise ValueError("message_id cannot be None.")

        return self._client.get_message(thread_id, message_id, correlation_vector=correlation_vector, **kwargs)

    @distributed_trace
    def list_messages(
        self,
        thread_id,  # type: str
        page_size=None,  # type: Optional[int]
        start_time=None,  # type: Optional[int]
        sync_state=None,  # type: Optional[str]
        correlation_vector=None,  # type: Optional[str]
        **kwargs  # type: Any
    ):
        # type: (...) -> "models.ListMessagesResponse"
        """Gets a list of messages from a thread.

        Gets a list of messages from a thread.

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
        :param correlation_vector: Correlation vector, if a value is not provided a randomly generated
         correlation vector would be returned in the response header "MS-CV".
        :type correlation_vector: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: ListMessagesResponse, or the result of cls(response)
        :rtype: ~azure.communication.chat.models.ListMessagesResponse
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")

        return self._client.list_messages(
            thread_id,
            page_size=page_size,
            start_time=start_time,
            sync_state=sync_state,
            correlation_vector=correlation_vector,
            **kwargs)

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

        Updates a message.

        :param thread_id: The thread id to which the message was sent.
        :type thread_id: str
        :param message_id: The message id.
        :type message_id: str
        :param update_message_request: Details of the request to update the message.
        :type update_message_request: ~azure.communication.chat.models.UpdateMessageRequest
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
        if not message_id:
            raise ValueError("message_id cannnot be None.")
        if not update_message_request:
            raise ValueError("update_message_request cannot be None.")

        return self._client.update_message(thread_id, message_id, correlation_vector, update_message_request, **kwargs)

    def delete_message(
        self,
        thread_id,  # type: str
        message_id,  # type: str
        correlation_vector=None,  # type: Optional[str]
        **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Deletes a message.

        Deletes a message.

        :param thread_id: The thread id to which the message was sent.
        :type thread_id: str
        :param message_id: The message id.
        :type message_id: str
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
        if not message_id:
            raise ValueError("message_id cannnot be None.")

        return self._client.delete_message(thread_id, message_id, correlation_vector, **kwargs)

    def close(self):
        # type: () -> None
        """Close the :class:`~azure.communication.chat.ChatClient` session.
        """
        return self._client.close()

    def __enter__(self):
        # type: () -> ChatClient
        self._client.__enter__()  # pylint:disable=no-member
        return self

    def __exit__(self, *args):
        # type: (*Any) -> None
        self._client.__exit__(*args)  # pylint:disable=no-member
