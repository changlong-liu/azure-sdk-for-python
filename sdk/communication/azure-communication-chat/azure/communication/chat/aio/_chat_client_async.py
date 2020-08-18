# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from azure.core.tracing.decorator_async import distributed_trace_async
from .._chat_client import ChatClient as ChatClientBase
from .._generated.aio import AzureCommunicationChatService
from .._generated.models import CreateChatThreadRequest
from .._common import CommunicationUserCredential, CommunicationUserCredentialPolicy
from ._chat_thread_client_async import ChatThreadClient

POLLING_INTERVAL = 5


class ChatClient(ChatClientBase):
    """A client to interact with the AzureCommunicationService Chat gateway.

    This client provides operations to create a chat thread, delete a thread,
    get thread by id, get threads, add member to thread, remove member from
    thread, send message, delete message, update message.

    :param str endpoint:
        The endpoint of the Azure Communication resource.
    :param str credential:
        The credentials with which to authenticate. The value is an User
        Access Token
    :keyword int polling_interval:
        Default waiting time between two polls for LRO operations if no
        Retry-After header is present.
    """
    def __init__(
            self, endpoint,  # type: str
            credential,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        polling_interval = kwargs.pop("polling_interval", POLLING_INTERVAL)

        super(ChatClient, self).__init__(
            endpoint,
            credential,
            polling_interval=polling_interval,
            **kwargs)

        self._client = AzureCommunicationChatService(
            endpoint,
            authentication_policy=CommunicationUserCredentialPolicy(CommunicationUserCredential(self._credential)),
            polling_interval=polling_interval,
            **kwargs)

    @distributed_trace_async
    async def create_thread(
            self, topic,  # type: str
            thread_members,  # type: list[ThreadMember]
            **kwargs  # type: Any
    ):
        # type: (...) -> ChatThreadClient
        """Creates a chat thread.

        :param topic: Required. The thread topic.
        :type topic: str
        :param thread_members: Required. Members to be added to the thread.
        :type thread_members: list[~azure.communication.chat.models.ThreadMember]
        :return: ChatThreadClient
        :rtype: ~azure.communication.chat.ChatThreadClient
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """
        if not topic:
            raise ValueError("topic cannot be None.")
        if not thread_members:
            raise ValueError("List of ThreadMember cannot be None.")

        create_thread_request = CreateChatThreadRequest(topic=topic, members=thread_members)

        create_thread_result = None
        try:
            create_thread_result = await self._client.create_chat_thread(create_thread_request, **kwargs)
        except:
            raise

        thread_id = create_thread_result.id

        return ChatThreadClient(
            thread_id=thread_id,
            endpoint=self._endpoint,
            credential=self._credential,
            polling_interval=self._polling_interval
        )

    async def __aenter__(self):
        # type: () -> ChatClient
        await self._client.__aenter__()  # pylint:disable=no-member
        return self

    async def __aexit__(self, *args):
        # type: (*Any) -> None
        await self._client.__aexit__(*args)  # pylint:disable=no-member
