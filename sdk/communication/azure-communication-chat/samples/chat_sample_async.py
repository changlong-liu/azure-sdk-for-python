# coding: utf-8

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


import os
import asyncio
import jwt


class ChatSamplesAsync(object):
    endpoint = os.environ.get("AZURE_COMMUNICATION_SERVICE_ENDPOINT", None)
    if not endpoint:
        raise ValueError("Set AZURE_COMMUNICATION_SERVICE_ENDPOINT env before run this sample.")
    skype_token = os.environ.get("TOKEN", None)
    if not skype_token:
        raise ValueError("Set TOKEN env before run this sample.")

    _thread_id = None
    _thread_creator = None
    _message_id = None

    async def create_thread_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.communication.chat.models import ThreadMember
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)

        # the user who makes the request must be in the member list of the CreateThreadRequest
        user_id = "8:" + jwt.decode(self.skype_token, verify=False)['skypeid']
        self._thread_creator = user_id

        create_thread_response = None
        async with chat_client:
            try:
                topic="test topic",
                members=[ThreadMember(
                    id=user_id,
                    display_name='name',
                    share_history_time='0'
                )]
                create_thread_response = await chat_client.create_chat_thread(topic, members)

            except HttpResponseError as e:
                print(e)
                return

        self._thread_id = create_thread_response.id
        print("thread created, id: " + self._thread_id)

    async def get_thread_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)

        thread = None
        async with chat_client:
            try:
                thread = await chat_client.get_chat_thread(self._thread_id)
            except HttpResponseError as e:
                print(e)
                return

        print("get_thread succeeded, thread id: " + thread.id + ", thread topic: " + thread.topic)

    async def update_thread_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)

        async with chat_client:
            try:
                topic = "update topic"
                await chat_client.update_chat_thread(self._thread_id, topic)
            except HttpResponseError as e:
                print(e)
                return

        print("update_thread succeeded")

    async def delete_thread_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)

        async with chat_client:
            try:
                await chat_client.delete_chat_thread(self._thread_id)
            except HttpResponseError as e:
                print(e)
                return

        print("delete_thread succeeded")

    async def send_message_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.communication.chat.models import MessagePriority
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)
        create_message_response = None

        async with chat_client:
            try:
                priority=MessagePriority.NORMAL
                content='hello world'
                sender_display_name='sender name'

                create_message_response = await chat_client.send_chat_message(
                    self._thread_id,
                    content,
                    priority=priority,
                    sender_display_name=sender_display_name)
            except HttpResponseError as e:
                print(e)
                return

        self._message_id = create_message_response.id
        print("send_message succeeded, message id:", self._message_id)

    async def get_message_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)
        message = None

        async with chat_client:
            try:
                message = await chat_client.get_chat_message(self._thread_id, self._message_id)
            except HttpResponseError as e:
                print(e)
                return

        print("get_message succeeded, message id:", message.id, \
            "content: ", message.content)

    async def list_messages_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)
        list_messages_response = None

        async with chat_client:
            try:
                list_messages_response = await chat_client.list_chat_messages(self._thread_id)
            except HttpResponseError as e:
                print(e)
                return

        print("list_messages succeeded, messages count:",
            len([elem for elem in list_messages_response.messages if elem.message_type == 'Text']))

    async def update_message_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)

        async with chat_client:
            try:
                content = "updated message content"
                await chat_client.update_chat_message(self._thread_id, self._message_id, content)
            except HttpResponseError as e:
                print(e)
                return

        print("update_message succeeded")

    async def send_read_receipt_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)

        async with chat_client:
            try:
                await chat_client.send_read_receipt(self._thread_id, self._message_id)
            except HttpResponseError as e:
                print(e)
                return

        print("send_read_receipt succeeded")

    async def list_read_receipts_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)

        read_receipts = []
        async with chat_client:
            try:
                read_receipts = await chat_client.list_read_receipts(self._thread_id)
            except HttpResponseError as e:
                print(e)
                return

        print("list_read_receipts succeeded, receipts:")
        for read_receipt in read_receipts:
            print(read_receipt)

    async def delete_message_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)

        async with chat_client:
            try:
                await chat_client.delete_chat_message(self._thread_id, self._message_id)
            except HttpResponseError as e:
                print(e)
                return

        print("delete_message succeeded")

    async def list_members_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)

        members = []
        async with chat_client:
            try:
                members = await chat_client.list_chat_members(self._thread_id)
            except HttpResponseError as e:
                print(e)
                return

        print("list_members succeeded, members:")
        for member in members:
            print(member)

    async def add_members_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.communication.chat.models import ThreadMember
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)

        # the new member must has the same resource id as the thread creator
        new_member_id = \
            self._thread_creator[:self._thread_creator.rfind("_")] + "_" \
            + "123456-0000123456"
        new_member = ThreadMember(
                id=new_member_id,
                display_name='name',
                share_history_time='0')
        members = [new_member]

        async with chat_client:
            try:
                await chat_client.add_chat_members(self._thread_id, members)
            except HttpResponseError as e:
                print(e)
                return

        print("add_members succeeded")

    async def remove_member_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)

        # this member was added when calling add_members()
        added_member_id = \
            self._thread_creator[:self._thread_creator.rfind("_")] + "_" \
            + "123456-0000123456"

        async with chat_client:
            try:
                await chat_client.remove_chat_member(self._thread_id, added_member_id)
            except HttpResponseError as e:
                print(e)
                return

        print("remove_member_async succeeded")

    async def send_typing_notification_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)

        async with chat_client:
            try:
                await chat_client.send_typing_notification(self._thread_id)
            except HttpResponseError as e:
                print(e)
                return

        print("send_typing_notification succeeded")

async def main():
    sample = ChatSamplesAsync()
    await sample.create_thread_async()
    await sample.get_thread_async()
    await sample.update_thread_async()
    await sample.send_message_async()
    await sample.get_message_async()
    await sample.list_messages_async()
    await sample.update_message_async()
    await sample.send_read_receipt_async()
    await sample.list_read_receipts_async()
    await sample.delete_message_async()
    await sample.add_members_async()
    await sample.list_members_async()
    await sample.remove_member_async()
    await sample.send_typing_notification_async()
    await sample.delete_thread_async()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())