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
        body,  # type: "models.CreateThreadRequest"
        correlation_vector=None,  # type: Optional[str]
        **kwargs  # type: **Any -> Dict[str, str]
    ):
        # type: (...) -> "models.CreateThreadResponse"
        """Creates a chat thread.

        Creates a chat thread.

        :param correlation_vector: Correlation vector, if a value is not provided a randomly generated
         correlation vector would be returned in the response header "MS-CV".
        :type correlation_vector: str
        :param body: Request payload for creating a chat thread.
        :type body: ~azure.communication.chat.models.CreateThreadRequest
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: CreateThreadResponse, or the result of cls(response)
        :rtype: ~azure.communication.chat.models.CreateThreadResponse
        :raises: ~azure.core.exceptions.HttpResponseError

        """
        # type: (request, models.CreateThreadRequest)
        if not body:
            raise ValueError("CreateThreadRequest cannot be None.")

        return self._client.create_thread(correlation_vector, body, **kwargs)

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
