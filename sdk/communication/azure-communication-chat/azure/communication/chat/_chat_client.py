# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from urllib.parse import urlparse
from azure.core.tracing.decorator import distributed_trace

from ._generated import models
from ._generated import AzureCommunicationChatService

POLLING_INTERVAL = 5


class ChatClient(object):
    """A client to interact with the AzureCommunicationService Chat gateway.

    This client provides operations to create a chat thread, delete a thread,
    get thread by id, get threads, add member to thread, remove member from
    thread, send message, delete message, update message.

    :param credential: Credential needed for the client to connect to Azure.
    :type credential: ~azure.core.credentials.AzureKeyCredential
    :param endpoint: The endpoint of the Azure Communication resource.
    :type endpoint: str
    :keyword int polling_interval: Default waiting time between two polls for LRO operations if no Retry-After header is present.
    """

    def __init__(
            self, 
            credential,  # type: "AzureKeyCredential"
            endpoint,  # type: str
            **kwargs  # type: Any
    ):
        try:
            if not endpoint.lower().startswith('http'):
                endpoint = "https://" + endpoint
        except AttributeError:
            raise ValueError("Host URL must be a string")

        parsed_url = urlparse(endpoint.rstrip('/'))
        if not parsed_url.netloc:
            raise ValueError("Invalid URL: {}".format(endpoint))

        polling_interval = kwargs.pop("polling_interval", POLLING_INTERVAL)

        self._client = AzureCommunicationChatService(
            credential,
            endpoint,
            polling_interval=polling_interval,
            name="Authorization", #work around of https://github.com/Azure/autorest.python/issues/735
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
