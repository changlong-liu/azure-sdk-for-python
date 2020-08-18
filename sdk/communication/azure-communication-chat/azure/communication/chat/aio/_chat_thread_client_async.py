# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from .._chat_thread_client import ChatThreadClient as ChatThreadClientBase
from .._generated.aio import AzureCommunicationChatService
from .._common import CommunicationUserCredential, CommunicationUserCredentialPolicy

POLLING_INTERVAL = 5


class ChatThreadClient(ChatThreadClientBase):
    """A client to interact with the AzureCommunicationService Chat gateway.
    Instances of this class is normally created by ChatClient.create_thread()

    This client provides operations to add member to chat thread, remove member from
    chat thread, send message, delete message, update message, send typing notifications,
    send and list read receipt

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
            thread_id,  # type: str
            endpoint,  # type: str
            credential,  # type: str
            **kwargs  # type: Any
    ):
        # type: (...) -> None
        polling_interval = kwargs.pop("polling_interval", POLLING_INTERVAL)
        super(ChatThreadClient, self).__init__(
            thread_id,
            endpoint,
            credential,
            polling_interval=polling_interval,
            **kwargs)

        self._client = AzureCommunicationChatService(
            endpoint,
            authentication_policy=CommunicationUserCredentialPolicy(CommunicationUserCredential(credential)),
            polling_interval=polling_interval,
            **kwargs)

    async def __aenter__(self):
        # type: () -> ChatClient
        await self._client.__aenter__()  # pylint:disable=no-member
        return self

    async def __aexit__(self, *args):
        # type: (*Any) -> None
        await self._client.__aexit__(*args)  # pylint:disable=no-member