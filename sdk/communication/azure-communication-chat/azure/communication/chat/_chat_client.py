# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from urllib.parse import urlparse
from msrest.service_client import ServiceClient
from msrest.authentication import ApiKeyCredentials
from ._generated import models
from ._generated import AzureCommunicationChatService


class ChatClient():
    """A client to interact with the AzureCommunicationService Chat gateway.

    This client provides operations to create a chat thread, delete a thread,
    get thread by id, get threads, add member to thread, remove member from
    thread, send message, delete message, update message.

    :param str host:
        The URL to AzureCommunicationService resource
    :param credential:
        The credentials with which to authenticate.

    """

    def __init__(
            self, url,  # type: str
            credential,  # type: Optional[Any]
            **kwargs  # type: Any
            ):
        try:
            if not url.lower().startswith('http'):
                url = "https://" + url
        except AttributeError:
            raise ValueError("Host URL must be a string")
        parsed_url = urlparse(url.rstrip('/'))
        if not parsed_url.netloc:
            raise ValueError("Invalid URL: {}".format(url))
        self._chat_service = AzureCommunicationChatService(url)
        self._chat_service.config.base_url = url
        crdes = ApiKeyCredentials(in_headers={"Authorization": credential})
        self._chat_service._client = ServiceClient(
            crdes,
            self._chat_service.config)
        #self._credential = credential

    @classmethod
    def from_credential(
            cls, url,  # type: str
            credential,  # type: str
            **kwargs  # type: Any
            ):  # type: (...) -> ChatClient
        """Create ChatClient from a Connection String.

        :param str url:
            A connection string to an Azure Storage account.
        :param str credential:
            The credentials with which to authenticate.
        :returns: A Chat client.
        :rtype: ~azure.communication.chat.ChatClient
        """
        return cls(url, credential, **kwargs)

    @distributed_trace
    def create_thread(self, topic, members, is_sticky_thread=None):
        """Creates a chat thread.

        :param topic: The thread topic.
        :type topic: str
        :type members: list[~azure.communication.chat.models.ThreadMember]
        :param correlation_vector: Correlation vector, if a value is not
         provided a randomly generated correlation vector would be returned in
         the response header "MS-CV".
        :type correlation_vector: str
        :param is_sticky_thread: Flag if a thread is sticky - sticky thread
         has an immutable member list, members cannot be added or removed.
         Sticky threads are only supported for 1-1 chat, i.e. with only two
         members.
        :type is_sticky_thread: bool
        """
        # type: (request, models.CreateThreadRequest)
        return self._chat_service.create_thread(topic, members, is_sticky_thread)
