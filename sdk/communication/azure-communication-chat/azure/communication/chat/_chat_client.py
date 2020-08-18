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
from ._utils import _to_utc_datetime

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar, Union
    from datetime import datetime


class ChatClient(object):
    """A client to interact with the AzureCommunicationService Chat gateway.

    This client provides operations to create a chat thread, delete a chat thread,
    get chat thread by id, list chat threads.

    :param str endpoint:
        The endpoint of the Azure Communication resource.
    :param str credential:
        The credentials with which to authenticate. The value is an User
        Access Token
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
            endpoint,
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
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")

        return ChatThreadClient(
            thread_id=thread_id,
            endpoint=self._endpoint,
            credential=self._credential,
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
        :type thread_members: list[~azure.communication.chat.models.ChatThreadMember]
        :return: ChatThreadClient
        :rtype: ~azure.communication.chat.ChatThreadClient
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not topic:
            raise ValueError("topic cannot be None.")
        if not thread_members:
            raise ValueError("List of ThreadMember cannot be None.")

        create_thread_request = CreateChatThreadRequest(topic=topic, members=thread_members)

        create_chat_thread_result = None
        try:
            create_chat_thread_result = self._client.create_chat_thread(create_thread_request, **kwargs)
        except:
            raise

        thread_id = create_chat_thread_result.id

        return ChatThreadClient(
            thread_id=thread_id,
            endpoint=self._endpoint,
            credential=self._credential,
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
        :rtype: ~azure.communication.chat.models.ChatThread
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")

        return self._client.get_chat_thread(thread_id, **kwargs)

    @distributed_trace
    def list_threads(
        self,
        **kwargs
    ):
        # type: (...) -> ListChatThreadsResult
        """Gets the list of chat threads of a user.

        :keyword int page_size: The number of threads being requested.
        :keyword ~datetime.datetime start_time: The start time(UTC) where the range query.
        :keyword str sync_state: The continuation token that previous request obtained. This is used for
         paging.
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: ListChatThreadsResult, or the result of cls(response)
        :rtype: ~azure.communication.chat.models.ListChatThreadsResult
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        page_size = kwargs.pop("page_size", None)
        start_time = kwargs.pop("start_time", None)
        sync_state = kwargs.pop("sync_state", None)

        return self._client.list_chat_threads(
            page_size=page_size,
            start_time=start_time,
            sync_state=sync_state,
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
        """
        if not thread_id:
            raise ValueError("thread_id cannot be None.")

        return self._client.delete_chat_thread(thread_id, **kwargs)

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
