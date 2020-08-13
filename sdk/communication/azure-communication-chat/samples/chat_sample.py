
# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: chat_sample.py
DESCRIPTION:
    These samples demonstrate chat operations.

    ///use ChatClient to perform a chatting sencario, like
    create thread, send message, add members, etc///
USAGE:
    chat_sample.py
"""


import jwt
import os


class ChatSamples(object):
    endpoint = os.environ.get("AZURE_COMMUNICATION_SERVICE_ENDPOINT", None)
    if not endpoint:
        raise ValueError("Set AZURE_COMMUNICATION_SERVICE_ENDPOINT env before run this sample.")
    token = os.environ.get("TOKEN", None)
    if not token:
        raise ValueError("Set TOKEN env before run this sample.")

    _thread_id = None
    _thread_creator = None
    _message_id = None
    _client_message_id = None

    def create_thread(self):
        from azure.communication.chat import ChatClient
        from azure.communication.chat import CreateThreadRequest, ThreadMember
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        # the user who makes the request must be in the member list of the CreateThreadRequest
        user_id = "8:" + jwt.decode(self.token, verify=False)['skypeid']
        self._thread_creator = user_id

        body = CreateThreadRequest(
            topic="test topic",
            members=[ThreadMember(
                id=user_id,
                display_name='name',
                member_role='Admin',
                share_history_time='0'
            )],
            is_sticky_thread=False
        )

        create_thread_response = None
        try:
            create_thread_response = chat_client.create_chat_thread(body)
        except HttpResponseError as e:
            print(e)
            return

        self._thread_id = create_thread_response.id
        print("thread created, id: " + self._thread_id)

    def get_thread(self):
        from azure.communication.chat import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        thread = None
        try:
            thread = chat_client.get_thread(self._thread_id)
        except HttpResponseError as e:
            print(e)
            return

        print("get_thread succeded, thread id: " + thread.id + ", thread topic: " + thread.topic)

    def update_thread(self):
        from azure.communication.chat import ChatClient
        from azure.communication.chat import UpdateThreadRequest
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        thread = None
        try:
            update_thread_request = UpdateThreadRequest(topic="update topic")
            chat_client.update_thread(self._thread_id, update_thread_request)
        except HttpResponseError as e:
            print(e)
            return

        print("update_thread succeded")

    def delete_thread(self):
        from azure.communication.chat import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        thread = None
        try:
            chat_client.delete_thread(self._thread_id)
        except HttpResponseError as e:
            print(e)
            return

        print("delete_thread succeded")

    def send_message(self):
        from azure.communication.chat import ChatClient
        from azure.communication.chat import CreateMessageRequest, MessagePriority
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        thread = None
        try:
            create_message_request = CreateMessageRequest(
                client_message_id='1581637626706',
                priority=MessagePriority.NORMAL,
                content='hello world',
                sender_display_name='sender name',
            )
            create_message_response = chat_client.send_message(self._thread_id, create_message_request)
        except HttpResponseError as e:
            print(e)
            return

        self._message_id = create_message_response.id
        self._client_message_id = create_message_response.client_message_id
        print("send_message succeded, message id:", self._message_id)

    def get_message(self):
        from azure.communication.chat import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        message = None
        try:
            message = chat_client.get_message(self._thread_id, self._message_id)
        except HttpResponseError as e:
            print(e)
            return

        print("get_message succeded, message id:", message.id, "client message id:" + message.client_message_id)

    def list_messages(self):
        from azure.communication.chat import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        list_messages_response = None
        try:
            list_messages_response = chat_client.list_messages(self._thread_id)
        except HttpResponseError as e:
            print(e)
            return

        print("list_messages succeded, messages count:",
            len([elem for elem in list_messages_response.messages if elem.message_type == 'Text']))

    def update_message(self):
        from azure.communication.chat import ChatClient
        from azure.communication.chat import UpdateMessageRequest
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        try:
            update_message_request = UpdateMessageRequest(content="updated message content")
            chat_client.update_message(self._thread_id, self._message_id, update_message_request)
        except HttpResponseError as e:
            print(e)
            return

        print("update_message succeded")

    def send_read_receipt(self):
        from azure.communication.chat import ChatClient
        from azure.communication.chat import PostReadReceiptRequest
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        try:
            post_read_receipt_request = PostReadReceiptRequest(
                client_message_id=self._client_message_id,
                message_id=self._message_id
                )
            chat_client.send_read_receipt(self._thread_id, post_read_receipt_request)
        except HttpResponseError as e:
            print(e)
            return

        print("send_read_receipt succeded")

    def list_read_receipts(self):
        from azure.communication.chat import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        read_receipts = []
        try:
            read_receipts = chat_client.list_read_receipts(self._thread_id)
        except HttpResponseError as e:
            print(e)
            return

        print("list_read_receipts succeded, receipts:")
        for read_receipt in read_receipts:
            print(read_receipt)

    def delete_message(self):
        from azure.communication.chat import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        try:
            chat_client.delete_message(self._thread_id, self._message_id)
        except HttpResponseError as e:
            print(e)
            return

        print("delete_message succeded")

    def list_members(self):
        from azure.communication.chat import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        members = []
        try:
            members = chat_client.list_members(self._thread_id)
        except HttpResponseError as e:
            print(e)
            return

        print("list_members succeded, members: ")
        for member in members:
            print(member)

    def add_members(self):
        from azure.communication.chat import ChatClient, ThreadMember
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        # the new member must has the same resource id as the thread creator
        new_member_id = \
            self._thread_creator[:self._thread_creator.rfind("_")] + "_" \
            + "123456-0000123456"
        new_member = ThreadMember(
                id=new_member_id,
                display_name='name',
                member_role='Admin',
                share_history_time='0')
        thread_members = [new_member]

        try:
            chat_client.add_members(self._thread_id, thread_members)
        except HttpResponseError as e:
            print(e)
            return

        print("add_members succeded")

    def remove_member(self):
        from azure.communication.chat import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        # this member was added when calling add_members()
        added_member_id = \
            self._thread_creator[:self._thread_creator.rfind("_")] + "_" \
            + "123456-0000123456"

        try:
            chat_client.remove_member(self._thread_id, added_member_id)
        except HttpResponseError as e:
            print(e)
            return

        print("remove_member succeded")

    def send_typing_notification(self):
        from azure.communication.chat import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        try:
            chat_client.send_typing_notification(self._thread_id)
        except HttpResponseError as e:
            print(e)
            return

        print("send_typing_notification succeded")

if __name__ == '__main__':
    sample = ChatSamples()
    sample.create_thread()
    sample.get_thread()
    sample.update_thread()
    sample.send_message()
    sample.get_message()
    sample.list_messages()
    sample.update_message()
    sample.send_read_receipt()
    sample.list_read_receipts()
    sample.delete_message()
    sample.list_members()
    sample.add_members()
    sample.remove_member()
    sample.send_typing_notification()
    sample.delete_thread()