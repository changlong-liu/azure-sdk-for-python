# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from .._chat_client import ChatClient as ChatClientBase
from .._generated.aio import AzureCommunicationChatService
from .._common import CommunicationUserCredentialPolicy

POLLING_INTERVAL = 5


class ChatClient(ChatClientBase):
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
        super(ChatClient, self).__init__(token, endpoint, **kwargs)

        self._client = AzureCommunicationChatService(
            endpoint,
            polling_interval=self._polling_interval,
            authentication_policy=CommunicationUserCredentialPolicy(self._credential),
            **kwargs
        )

    async def close(self):
        # type: () -> None
        """Close the :class:`~azure.communication.chat.aio.ChatClient` session.
        """
        return await self._client.close()

    async def __aenter__(self):
        # type: () -> ChatClient
        await self._client.__aenter__()  # pylint:disable=no-member
        return self

    async def __aexit__(self, *args):
        # type: (*Any) -> None
        await self._client.__aexit__(*args)  # pylint:disable=no-member