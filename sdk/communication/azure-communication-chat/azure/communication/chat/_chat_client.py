from urllib.parse import urlparse
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
        self._client = AzureCommunicationChatService(parsed_url)
        self._credential = credential

    @classmethod
    def from_skype_token(
            cls, url,  # type: str
            credential,  # type: Optional[Any]
            **kwargs  # type: Any
            ):  # type: (...) -> ChatClient
        """Create ChatClient from a Connection String.

        :param str url:
            A connection string to an Azure Storage account.
        :param credential:
            The credentials with which to authenticate.
        :returns: A Chat client.
        :rtype: ~azure.communication.chat.ChatClient
        """
        return cls(url, credential, **kwargs)
