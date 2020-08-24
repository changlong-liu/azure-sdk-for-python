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

from ._chat_thread_client import ChatThreadClient
from ._common import CommunicationUserCredential, CommunicationUserCredentialPolicy
from ._generated import AzureCommunicationChatService
from ._generated.models import CreateChatThreadRequest
from ._utils import _to_utc_datetime # pylint: disable=unused-import

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar, Union
    from datetime import datetime


class ChatClient(object):
    """A client to interact with the AzureCommunicationService Chat gateway.

    This client provides operations to create chat thread, delete chat thread,
    get chat thread by id, list chat threads, create chat thread client.

    :param str endpoint:
        The endpoint of the Azure Communication resource.
    :param str credential:
        The credentials with which to authenticate. The value is an User
        Access Token

    .. admonition:: Example:

        .. literalinclude:: ../samples/chat_client_sample.py
            :start-after: [START create_chat_client]
            :end-before: [END create_chat_client]
            :language: python
            :dedent: 8
            :caption: Creating the ChatClient from a URL and token.
    """
    def __init__(
            self,
            endpoint,  # type: str
            credential,  # type: str
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

        self._endpoint = endpoint
        self._credential = credential

        self._client = AzureCommunicationChatService(
            self._endpoint,
            authentication_policy=CommunicationUserCredentialPolicy(CommunicationUserCredential(credential)),
            **kwargs
        )

    @distributed_trace
    def get_chat_thread_client(
        self, thread_id, # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> ChatThreadClient
        """
        Get ChatThreadClient by providing a thread_id.

        :param thread_id: Required. The thread id.
        :type thread_id: str
        :return: ChatThreadClient
        :rtype: ~azure.communication.chat.ChatThreadClient
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError

        .. admonition:: Example:

            .. literalinclude:: ../samples/chat_client_sample.py
                :start-after: [START get_chat_thread_client]
                :end-before: [END get_chat_thread_client]
                :language: python
                :dedent: 8
                :caption: Creating the ChatThreadClient from an existing chat thread id.
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")

        return ChatThreadClient(
            endpoint=self._endpoint,
            credential=self._credential,
            thread_id=thread_id,
            **kwargs
        )

    @distributed_trace
    def create_thread(
            self, topic,  # type: str
            thread_members,  # type: list[ChatThreadMember]
            **kwargs  # type: Any
    ):
        # type: (...) -> ChatThreadClient
        """Creates a chat thread.

        :param topic: Required. The thread topic.
        :type topic: str
        :param thread_members: Required. Members to be added to the thread.
        :type thread_members: list[~azure.communication.chat.ChatThreadMember]
        :return: ChatThreadClient
        :rtype: ~azure.communication.chat.ChatThreadClient
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError

        .. admonition:: Example:

            .. literalinclude:: ../samples/chat_client_sample.py
                :start-after: [START create_thread]
                :end-before: [END create_thread]
                :language: python
                :dedent: 8
                :caption: Creating ChatThreadClient by creating a new chat thread.
        """
        if not topic:
            raise ValueError("topic cannot be None.")
        if not thread_members:
            raise ValueError("List of ThreadMember cannot be None.")

        create_thread_request = CreateChatThreadRequest(topic=topic, members=thread_members)

        create_chat_thread_result = self._client.create_chat_thread(create_thread_request, **kwargs)

        thread_id = create_chat_thread_result.id

        return ChatThreadClient(
            endpoint=self._endpoint,
            credential=self._credential,
            thread_id=thread_id,
            **kwargs
        )

    @distributed_trace
    def get_thread(
            self, thread_id,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> ChatThread
        """Gets a chat thread.

        :param thread_id: Required. Thread id to get.
        :type thread_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: ChatThread, or the result of cls(response)
        :rtype: ~azure.communication.chat.ChatThread
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError

        .. admonition:: Example:

            .. literalinclude:: ../samples/chat_client_sample.py
                :start-after: [START get_thread]
                :end-before: [END get_thread]
                :language: python
                :dedent: 8
                :caption: Getting a chat thread by thread id.
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")

        return self._client.get_chat_thread(thread_id, **kwargs)

    @distributed_trace
    def list_threads(
        self,
        **kwargs
    ):
        # type: (...) -> ItemPaged[ChatThreadInfo]
        """Gets the list of chat threads of a user.

        :keyword int page_size: The number of threads being requested.

        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: ItemPaged[:class:`~azure.communication.chat.ChatThreadInfo`]
        :rtype: ~azure.core.paging.ItemPaged
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError

        .. admonition:: Example:

            .. literalinclude:: ../samples/chat_client_sample.py
                :start-after: [START list_threads]
                :end-before: [END list_threads]
                :language: python
                :dedent: 8
                :caption: listing chat threads.
        """
        page_size = kwargs.pop("page_size", None)

        return self._client.list_chat_threads(
            cls=kwargs.pop("cls", lambda objs: [x for x in objs]),
            max_page_size=page_size,
            **kwargs)

    @distributed_trace
    def delete_thread(
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

        .. admonition:: Example:

            .. literalinclude:: ../samples/chat_client_sample.py
                :start-after: [START delete_thread]
                :end-before: [END delete_thread]
                :language: python
                :dedent: 8
                :caption: deleting chat thread.
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")

        return self._client.delete_chat_thread(thread_id, **kwargs)

    def close(self):
        # type: () -> None
        self._client.close()

    def __enter__(self):
        # type: () -> ChatClient
        self._client.__enter__()  # pylint:disable=no-member
        return self

    def __exit__(self, *args):
        # type: (*Any) -> None
        self._client.__exit__(*args)  # pylint:disable=no-member
