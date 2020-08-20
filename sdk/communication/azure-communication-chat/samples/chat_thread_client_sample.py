# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: chat_thread_client_sample.py
DESCRIPTION:
    These samples demonstrate create a chat thread client, to update
    chat thread, get chat message, list chat messages, update chat message, send
    read receipt, list read receipts, delete chat message, add members, remove
    members, list members, send typing notification
    You need to use azure.communication.configuration module to get user access
    token and user identity before run this sample

USAGE:
    python chat_thread_client_sample.py
    Set the environment variables with your own values before running the sample:
    1) AZURE_COMMUNICATION_SERVICE_ENDPOINT - Communication Service endpoint url
    2) TOKEN - the user access token, from token_response.token
    3) USER_ID - the user id, from token_response.identity
"""


import os

class ChatThreadClientSamples(object):
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
    _message_id = None
    _new_member_id = None

    def create_chat_thread_client(self):
        # [START create_chat_thread_client]
        from azure.communication.chat import ChatClient
        from azure.communication.chat.models import ChatThreadMember
        chat_client = ChatClient(self.endpoint, self.token)
        topic="test topic"
        members = [ChatThreadMember(
            id=self.user_id,
            display_name='name',
            share_history_time='0'
        )]
        chat_thread_client = chat_client.create_thread(topic, members)
        # [END create_chat_thread_client]
        self._thread_id = chat_thread_client.thread_id
        print("chat_thread_client created")

    def update_thread(self):
        from azure.communication.chat import ChatThreadClient
        chat_thread_client = ChatThreadClient(self._thread_id, self.endpoint, self.token)
        # [START update_thread]
        topic = "updated thread topic"
        chat_thread_client.update_thread(topic=topic)
        # [END update_thread]

        print("update_chat_thread succeeded")

    def send_message(self):
        from azure.communication.chat import ChatThreadClient
        chat_thread_client = ChatThreadClient(self._thread_id, self.endpoint, self.token)
        # [START send_message]
        from azure.communication.chat.models import ChatMessagePriority

        priority = ChatMessagePriority.NORMAL
        content = 'hello world'
        sender_display_name = 'sender name'

        send_message_result = chat_thread_client.send_message(
            content,
            priority=priority,
            sender_display_name=sender_display_name)
        # [END send_message]

        self._message_id = send_message_result.id
        print("send_chat_message succeeded, message id:", self._message_id)

    def get_message(self):
        from azure.communication.chat import ChatThreadClient
        chat_thread_client = ChatThreadClient(self._thread_id, self.endpoint, self.token)
        # [START get_message]
        chat_message = chat_thread_client.get_message(self._message_id)
        # [END get_message]

        print("get_chat_message succeeded, message id:", chat_message.id, \
            "content: ", chat_message.content)

    def list_messages(self):
        from azure.communication.chat import ChatThreadClient
        chat_thread_client = ChatThreadClient(self._thread_id, self.endpoint, self.token)
        # [START list_messages]
        list_chat_messages_result = chat_thread_client.list_messages()
        # [END list_messages]

        messages = [elem for elem in list_chat_messages_result.messages if elem.type == 'Text']
        print("list_chat_messages succeeded, messages count:", len(messages))
        for msg in messages:
            print(msg)

    def update_message(self):
        from azure.communication.chat import ChatThreadClient
        chat_thread_client = ChatThreadClient(self._thread_id, self.endpoint, self.token)
        # [START update_message]
        content = "updated content"
        chat_thread_client.update_message(self._message_id, content=content)
        # [END update_message]

        print("update_chat_message succeeded")

    def send_read_receipt(self):
        from azure.communication.chat import ChatThreadClient
        chat_thread_client = ChatThreadClient(self._thread_id, self.endpoint, self.token)
        # [START send_read_receipt]
        chat_thread_client.send_read_receipt(self._message_id)
        # [END send_read_receipt]

        print("send_read_receipt succeeded")

    def list_read_receipts(self):
        from azure.communication.chat import ChatThreadClient
        chat_thread_client = ChatThreadClient(self._thread_id, self.endpoint, self.token)
        # [START list_read_receipts]
        read_receipts = chat_thread_client.list_read_receipts()
        # [END list_read_receipts]

        print("list_read_receipts succeeded, receipts:")
        for read_receipt in read_receipts:
            print(read_receipt)

    def delete_message(self):
        from azure.communication.chat import ChatThreadClient
        chat_thread_client = ChatThreadClient(self._thread_id, self.endpoint, self.token)
        # [START delete_message]
        chat_thread_client.delete_message(self._message_id)
        # [END delete_message]

        print("delete_chat_message succeeded")

    def list_members(self):
        from azure.communication.chat import ChatThreadClient
        chat_thread_client = ChatThreadClient(self._thread_id, self.endpoint, self.token)
        # [START list_members]
        chat_thread_members = chat_thread_client.list_members()
        # [END list_members]

        print("list_chat_members succeeded, members: ")
        for member in chat_thread_members:
            print(member)

    def add_members(self):
        from azure.communication.chat import ChatThreadClient
        chat_thread_client = ChatThreadClient(self._thread_id, self.endpoint, self.token)

        # the new member must has the same resource id as the thread creator
        new_member_id = \
            self.user_id[:self.user_id.rfind("_")] + "_" \
            + "123456-0000123456"
        self._new_member_id = new_member_id

        # [START add_members]
        from azure.communication.chat.models import ChatThreadMember
        new_member = ChatThreadMember(
                id=new_member_id,
                display_name='name',
                share_history_time='0')
        thread_members = [new_member]
        chat_thread_client.add_members(thread_members)
        # [END add_members]
        print("add_chat_members succeeded")

    def remove_member(self):
        from azure.communication.chat import ChatThreadClient
        chat_thread_client = ChatThreadClient(self._thread_id, self.endpoint, self.token)

        # this member was added when calling add_members()
        member_id = self._new_member_id

        # [START remove_member]
        chat_thread_client.remove_member(member_id)
        # [END remove_member]

        print("remove_chat_member succeeded")

    def send_typing_notification(self):
        from azure.communication.chat import ChatThreadClient
        chat_thread_client = ChatThreadClient(self._thread_id, self.endpoint, self.token)
        # [START send_typing_notification]
        chat_thread_client.send_typing_notification()
        # [END send_typing_notification]

        print("send_typing_notification succeeded")

if __name__ == '__main__':
    sample = ChatThreadClientSamples()
    sample.create_chat_thread_client()
    sample.update_thread()
    sample.send_message()
    sample.get_message()
    sample.list_messages()
    sample.update_message()
    sample.send_read_receipt()
    sample.list_read_receipts()
    sample.delete_message()
    sample.add_members()
    sample.list_members()
    sample.remove_member()
    sample.send_typing_notification()
