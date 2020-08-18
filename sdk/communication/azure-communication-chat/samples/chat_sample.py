
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
    user_id = os.environ.get("USER_ID", None)
    if not user_id:
        raise ValueError("Set USER_ID env before run this sample.")

    _thread_id = None
    _thread_creator = user_id
    _message_id = None
    _chat_thread_client = None

    def create_chat_thread(self):
        from azure.communication.chat import ChatClient
        from azure.communication.chat.models import ChatThreadMember
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.endpoint, self.token)

        topic="test topic"
        members = [ChatThreadMember(
            id=self._thread_creator,
            display_name='name',
            share_history_time='0'
        )]

        chat_thread_client = None
        try:
            chat_thread_client = chat_client.create_thread(topic, members)
        except HttpResponseError as e:
            print(e)
            return

        self._chat_thread_client = chat_thread_client
        self._thread_id = self._chat_thread_client.thread_id
        print("thread created, id: " + self._thread_id)

    def get_chat_thread(self):
        from azure.communication.chat import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.endpoint, self.token)

        chat_thread = None
        try:
            chat_thread = chat_client.get_thread(self._thread_id)
        except HttpResponseError as e:
            print(e)
            return

        print("get_chat_thread succeeded, thread id: " + chat_thread.id + ", thread topic: " + chat_thread.topic)

    def list_chat_threads(self):
        from azure.communication.chat import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.endpoint, self.token)

        list_chat_threads_result = None
        try:
            list_chat_threads_result = chat_client.list_threads()
        except HttpResponseError as e:
            print(e)
            return

        print("list_chat_threads succeeded, count of chat threads: ", len(list_chat_threads_result.threads))

    def update_chat_thread(self):
        from azure.core.exceptions import HttpResponseError

        try:
            topic = "updated thread topic"
            self._chat_thread_client.update_thread(topic=topic)
        except HttpResponseError as e:
            print(e)
            return

        print("update_chat_thread succeeded")

    def delete_chat_thread(self):
        from azure.communication.chat import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.endpoint, self.token)

        try:
            chat_client.delete_thread(self._thread_id)
        except HttpResponseError as e:
            print(e)
            return

        print("delete_chat_thread succeeded")

    def send_chat_message(self):
        from azure.communication.chat.models import ChatMessagePriorityDto
        from azure.core.exceptions import HttpResponseError

        send_message_result = None
        try:
            priority = ChatMessagePriorityDto.NORMAL
            content = 'hello world'
            sender_display_name = 'sender name'

            send_message_result = self._chat_thread_client.send_message(
                content,
                priority=priority,
                sender_display_name=sender_display_name)
        except HttpResponseError as e:
            print(e)
            return

        self._message_id = send_message_result.id
        print("send_chat_message succeeded, message id:", self._message_id)

    def get_chat_message(self):
        from azure.core.exceptions import HttpResponseError

        chat_message = None
        try:
            chat_message = self._chat_thread_client.get_message(self._message_id)
        except HttpResponseError as e:
            print(e)
            return

        print("get_chat_message succeeded, message id:", chat_message.id, \
            "content: ", chat_message.content)

    def list_chat_messages(self):
        from azure.core.exceptions import HttpResponseError

        list_chat_messages_result = None
        try:
            list_chat_messages_result = self._chat_thread_client.list_messages()
        except HttpResponseError as e:
            print(e)
            return

        print("list_chat_messages succeeded, messages count:",
            len([elem for elem in list_chat_messages_result.messages if elem.type == 'Text']))

    def update_chat_message(self):
        from azure.core.exceptions import HttpResponseError

        try:
            content = "updated content"
            self._chat_thread_client.update_message(self._message_id, content=content)
        except HttpResponseError as e:
            print(e)
            return

        print("update_chat_message succeeded")

    def send_read_receipt(self):
        from azure.core.exceptions import HttpResponseError

        try:
            self._chat_thread_client.send_read_receipt(self._message_id)
        except HttpResponseError as e:
            print(e)
            return

        print("send_read_receipt succeeded")

    def list_read_receipts(self):
        from azure.core.exceptions import HttpResponseError

        read_receipts = []
        try:
            read_receipts = self._chat_thread_client.list_read_receipts()
        except HttpResponseError as e:
            print(e)
            return

        print("list_read_receipts succeeded, receipts:")
        for read_receipt in read_receipts:
            print(read_receipt)

    def delete_chat_message(self):
        from azure.core.exceptions import HttpResponseError

        try:
            self._chat_thread_client.delete_message(self._message_id)
        except HttpResponseError as e:
            print(e)
            return

        print("delete_chat_message succeeded")

    def list_chat_members(self):
        from azure.core.exceptions import HttpResponseError

        chat_thread_members = []
        try:
            chat_thread_members = self._chat_thread_client.list_members()
        except HttpResponseError as e:
            print(e)
            return

        print("list_chat_members succeeded, members: ")
        for member in chat_thread_members:
            print(member)

    def add_chat_members(self):
        from azure.communication.chat.models import ChatThreadMember
        from azure.core.exceptions import HttpResponseError

        # the new member must has the same resource id as the thread creator
        new_member_id = \
            self._thread_creator[:self._thread_creator.rfind("_")] + "_" \
            + "123456-0000123456"
        new_member = ChatThreadMember(
                id=new_member_id,
                display_name='name',
                share_history_time='0')
        thread_members = [new_member]

        try:
            self._chat_thread_client.add_members(thread_members)
        except HttpResponseError as e:
            print(e)
            return

        print("add_chat_members succeeded")

    def remove_chat_member(self):
        from azure.core.exceptions import HttpResponseError

        # this member was added when calling add_members()
        added_member_id = \
            self._thread_creator[:self._thread_creator.rfind("_")] + "_" \
            + "123456-0000123456"

        try:
            self._chat_thread_client.remove_member(added_member_id)
        except HttpResponseError as e:
            print(e)
            return

        print("remove_chat_member succeeded")

    def send_typing_notification(self):
        from azure.core.exceptions import HttpResponseError

        try:
            self._chat_thread_client.send_typing_notification()
        except HttpResponseError as e:
            print(e)
            return

        print("send_typing_notification succeeded")

if __name__ == '__main__':
    sample = ChatSamples()
    sample.create_chat_thread()
    sample.update_chat_thread()
    sample.get_chat_thread()
    sample.list_chat_threads()
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
