
# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: chat_sample.py
DESCRIPTION:
    These samples demonstrate chat operations.

    ///use ChatClient to perform a chatting scenario, like
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

    def create_chat_thread(self):
        from azure.communication.chat import ChatClient
        from azure.communication.chat.models import ThreadMember
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        # the user who makes the request must be in the member list of the CreateThreadRequest
        user_id = "8:" + jwt.decode(self.token, verify=False)['skypeid']
        self._thread_creator = user_id

        topic="test topic"
        members = [ThreadMember(
            id=user_id,
            display_name='name',
            share_history_time='0'
        )]

        create_thread_result = None
        try:
            create_thread_result = chat_client.create_chat_thread(topic, members)
        except HttpResponseError as e:
            print(e)
            return

        self._thread_id = create_thread_result.id
        print("thread created, id: " + self._thread_id)

    def get_chat_thread(self):
        from azure.communication.chat import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        thread = None
        try:
            thread = chat_client.get_chat_thread(self._thread_id)
        except HttpResponseError as e:
            print(e)
            return

        print("get_chat_thread succeeded, thread id: " + thread.id + ", thread topic: " + thread.topic)

    def list_chat_threads(self):
        from azure.communication.chat import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        try:
            list_threads_result = chat_client.list_chat_threads()
        except HttpResponseError as e:
            print(e)
            return

        print("list_chat_threads succeeded, count of chat threads: ", len(list_threads_result.threads))

    def update_chat_thread(self):
        from azure.communication.chat import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        try:
            topic = "update topic"
            chat_client.update_chat_thread(self._thread_id, topic)
        except HttpResponseError as e:
            print(e)
            return

        print("update_chat_thread succeeded")

    def delete_chat_thread(self):
        from azure.communication.chat import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        try:
            chat_client.delete_chat_thread(self._thread_id)
        except HttpResponseError as e:
            print(e)
            return

        print("delete_chat_thread succeeded")

    def send_chat_message(self):
        from azure.communication.chat import ChatClient
        from azure.communication.chat.models import MessagePriority
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        try:
            priority = MessagePriority.NORMAL
            content = 'hello world'
            sender_display_name = 'sender name'

            create_message_result = chat_client.send_chat_message(
                self._thread_id,
                content,
                priority=priority,
                sender_display_name=sender_display_name)
        except HttpResponseError as e:
            print(e)
            return

        self._message_id = create_message_result.id
        print("send_chat_message succeeded, message id:", self._message_id)

    def get_chat_message(self):
        from azure.communication.chat import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        message = None
        try:
            message = chat_client.get_chat_message(self._thread_id, self._message_id)
        except HttpResponseError as e:
            print(e)
            return

        print("get_chat_message succeeded, message id:", message.id, \
            "content: ", message.content)

    def list_chat_messages(self):
        from azure.communication.chat import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        list_messages_response = None
        try:
            list_messages_response = chat_client.list_chat_messages(self._thread_id)
        except HttpResponseError as e:
            print(e)
            return

        print("list_chat_messages succeeded, messages count:",
            len([elem for elem in list_messages_response.messages if elem.message_type == 'Text']))

    def update_chat_message(self):
        from azure.communication.chat import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        try:
            content = "updated content"
            chat_client.update_chat_message(self._thread_id, self._message_id, content)
        except HttpResponseError as e:
            print(e)
            return

        print("update_chat_message succeeded")

    def send_read_receipt(self):
        from azure.communication.chat import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        try:
            chat_client.send_read_receipt(self._thread_id, self._message_id)
        except HttpResponseError as e:
            print(e)
            return

        print("send_read_receipt succeeded")

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

        print("list_read_receipts succeeded, receipts:")
        for read_receipt in read_receipts:
            print(read_receipt)

    def delete_chat_message(self):
        from azure.communication.chat import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        try:
            chat_client.delete_chat_message(self._thread_id, self._message_id)
        except HttpResponseError as e:
            print(e)
            return

        print("delete_chat_message succeeded")

    def list_chat_members(self):
        from azure.communication.chat import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        members = []
        try:
            members = chat_client.list_chat_members(self._thread_id)
        except HttpResponseError as e:
            print(e)
            return

        print("list_chat_members succeeded, members: ")
        for member in members:
            print(member)

    def add_chat_members(self):
        from azure.communication.chat import ChatClient
        from azure.communication.chat.models import ThreadMember
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        # the new member must has the same resource id as the thread creator
        new_member_id = \
            self._thread_creator[:self._thread_creator.rfind("_")] + "_" \
            + "123456-0000123456"
        new_member = ThreadMember(
                id=new_member_id,
                display_name='name',
                share_history_time='0')
        thread_members = [new_member]

        try:
            chat_client.add_chat_members(self._thread_id, thread_members)
        except HttpResponseError as e:
            print(e)
            return

        print("add_chat_members succeeded")

    def remove_chat_member(self):
        from azure.communication.chat import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        # this member was added when calling add_members()
        added_member_id = \
            self._thread_creator[:self._thread_creator.rfind("_")] + "_" \
            + "123456-0000123456"

        try:
            chat_client.remove_chat_member(self._thread_id, added_member_id)
        except HttpResponseError as e:
            print(e)
            return

        print("remove_chat_member succeeded")

    def send_typing_notification(self):
        from azure.communication.chat import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.token, self.endpoint)

        try:
            chat_client.send_typing_notification(self._thread_id)
        except HttpResponseError as e:
            print(e)
            return

        print("send_typing_notification succeeded")

if __name__ == '__main__':
    sample = ChatSamples()
    sample.create_chat_thread()
    sample.get_chat_thread()
    sample.list_chat_threads()
    sample.update_chat_thread()
    sample.send_chat_message()
    sample.get_chat_message()
    sample.list_chat_messages()
    sample.update_chat_message()
    sample.send_read_receipt()
    sample.list_read_receipts()
    sample.delete_chat_message()
    sample.add_chat_members()
    sample.list_chat_members()
    sample.remove_chat_member()
    sample.send_typing_notification()
    sample.delete_chat_thread()