
# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: chat_client_sample.py
DESCRIPTION:
    These samples demonstrate create a chat client, get a chat thread client,
    create a chat thread, get a chat thread by id, list chat threads, delete
    a chat thread by id.
    You need to use azure.communication.configuration module to get user access
    token and user identity before run this sample

USAGE:
    python chat_client_sample.py
    Set the environment variables with your own values before running the sample:
    1) AZURE_COMMUNICATION_SERVICE_ENDPOINT - Communication Service endpoint url
    2) TOKEN - the user access token, from token_response.token
    3) USER_ID - the user id, from token_response.identity
"""


import os

class ChatClientSamples(object):
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
    _chat_thread_client = None

    def create_chat_client(self):
        # [START create_chat_client]
        from azure.communication.chat import ChatClient
        chat_client = ChatClient(self.endpoint, self.token)
        # [END create_chat_client]

    def create_thread(self):
        # [START create_thread]
        from azure.communication.chat import ChatClient
        from azure.communication.chat import ChatThreadMember

        chat_client = ChatClient(self.endpoint, self.token)

        topic="test topic"
        members = [ChatThreadMember(
            id=self.user_id,
            display_name='name',
            share_history_time='0'
        )]
        chat_thread_client = chat_client.create_thread(topic, members)
        # [END create_thread]

        self._chat_thread_client = chat_thread_client
        self._thread_id = self._chat_thread_client.thread_id
        print("thread created, id: " + self._thread_id)

    def get_chat_thread_client(self):
        # [START get_chat_thread_client]
        from azure.communication.chat import ChatClient

        chat_client = ChatClient(self.endpoint, self.token)
        chat_thread_client = chat_client.get_chat_thread_client(self._thread_id)
        # [END get_chat_thread_client]

        print("chat_thread_client created with thread id: ", chat_thread_client.thread_id)

    def get_thread(self):
        # [START get_thread]
        from azure.communication.chat import ChatClient

        chat_client = ChatClient(self.endpoint, self.token)
        chat_thread = chat_client.get_thread(self._thread_id)
        # [END get_thread]

        print("get_thread succeeded, thread id: " + chat_thread.id + ", thread topic: " + chat_thread.topic)

    def list_threads(self):
        # [START list_threads]
        from azure.communication.chat import ChatClient

        chat_client = ChatClient(self.endpoint, self.token)
        chat_thread_infos = chat_client.list_threads(max_page_size=5)
        # [END list_threads]

        print("list_threads succeeded with max_page_size is 5")
        for chat_thread_info in chat_thread_infos:
            print(chat_thread_info)

    def delete_thread(self):
        # [START delete_thread]
        from azure.communication.chat import ChatClient

        chat_client = ChatClient(self.endpoint, self.token)
        chat_client.delete_thread(self._thread_id)
        # [END delete_thread]

        print("delete_thread succeeded")

if __name__ == '__main__':
    sample = ChatClientSamples()
    sample.create_chat_client()
    sample.create_thread()
    sample.get_chat_thread_client()
    sample.get_thread()
    sample.list_threads()
    sample.delete_thread()
