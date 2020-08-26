
# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: chat_client_sample_async.py
DESCRIPTION:
    These samples demonstrate create a chat client, get a chat thread client,
    create a chat thread, get a chat thread by id, list chat threads, delete
    a chat thread by id.
    You need to use azure.communication.configuration module to get user access
    token and user identity before run this sample

USAGE:
    python chat_client_sample_async.py
    Set the environment variables with your own values before running the sample:
    1) AZURE_COMMUNICATION_SERVICE_ENDPOINT - Communication Service endpoint url
    2) TOKEN - the user access token, from token_response.token
    3) USER_ID - the user id, from token_response.identity
"""

import os
import asyncio

class ChatClientSamplesAsync(object):
    endpoint = os.environ.get("AZURE_COMMUNICATION_SERVICE_ENDPOINT", None)
    if not endpoint:
        raise ValueError("Set AZURE_COMMUNICATION_SERVICE_ENDPOINT env before run this sample.")

    token = os.environ.get("TOKEN", None)
    if not token:
        raise ValueError("Set TOKEN env before run this sample.")

    user_id = os.environ.get("USER_ID", None)
    if not user_id:
        raise ValueError("Set USER_ID env before run this sample.")

    _thread_id = None

    def create_chat_client(self):
        # [START create_chat_client]
        from azure.communication.chat.aio import ChatClient
        chat_client = ChatClient(self.endpoint, self.token)
        # [END create_chat_client]
        print("chat_client created")

    async def create_thread_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.communication.chat import ChatThreadMember

        chat_client = ChatClient(self.endpoint, self.token)
        async with chat_client:
            # [START create_thread]
            topic="test topic"
            members = [ChatThreadMember(
                id=self.user_id
            )]
            chat_thread_client = await chat_client.create_chat_thread(topic, members)
            # [END create_thread]

            self._thread_id = chat_thread_client.thread_id
            print("thread created, id: " + self._thread_id)


    def get_chat_thread_client(self):
        # [START get_chat_thread_client]
        from azure.communication.chat.aio import ChatClient

        chat_client = ChatClient(self.endpoint, self.token)
        chat_thread_client = chat_client.get_chat_thread_client(self._thread_id)
        # [END get_chat_thread_client]

        print("chat_thread_client created with thread id: ", chat_thread_client.thread_id)

    async def get_thread_async(self):
        from azure.communication.chat.aio import ChatClient

        chat_client = ChatClient(self.endpoint, self.token)
        async with chat_client:
            # [START get_thread]
            chat_thread = await chat_client.get_chat_thread(self._thread_id)
            # [END get_thread]
            print("get_thread succeeded, thread id: " + chat_thread.id + ", thread topic: " + chat_thread.topic)

    async def list_threads_async(self):
        from azure.communication.chat.aio import ChatClient

        chat_client = ChatClient(self.endpoint, self.token)
        async with chat_client:
            # [START list_threads]
            chat_thread_infos = chat_client.list_chat_threads(max_page_size=5)
            print("list_threads succeeded with page_size is 5")
            async for chat_thread_page in chat_thread_infos.by_page():
                l = [ i async for i in chat_thread_page]
                print("page size: ", len(l))
            # [END list_threads]

    async def delete_thread_async(self):
        from azure.communication.chat.aio import ChatClient

        chat_client = ChatClient(self.endpoint, self.token)
        async with chat_client:
            # [START delete_thread]
            await chat_client.delete_chat_thread(self._thread_id)
            # [END delete_thread]
            print("delete_thread succeeded")

async def main():
    sample = ChatClientSamplesAsync()
    sample.create_chat_client()
    await sample.create_thread_async()
    sample.get_chat_thread_client()
    await sample.get_thread_async()
    await sample.list_threads_async()
    await sample.delete_thread_async()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
