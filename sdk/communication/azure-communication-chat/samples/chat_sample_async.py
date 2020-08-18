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

    async def create_thread_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.communication.chat.models import ChatThreadMember
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.endpoint, self.token)

        chat_thread_client = None
        async with chat_client:
            try:
                topic="test topic"
                members=[ChatThreadMember(
                    id=self._thread_creator,
                    display_name='name',
                    share_history_time='0'
                )]
                chat_thread_client = await chat_client.create_thread(topic, members)

            except HttpResponseError as e:
                print(e)
                return

        self._chat_thread_client = chat_thread_client
        self._thread_id = self._chat_thread_client.thread_id
        print("thread created, id: " + self._thread_id)

    async def get_thread_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.endpoint, self.token)

        chat_thread = None
        async with chat_client:
            try:
                chat_thread = await chat_client.get_thread(self._thread_id)
            except HttpResponseError as e:
                print(e)
                return

        print("get_thread succeeded, thread id: " + chat_thread.id + ", thread topic: " + chat_thread.topic)

    async def list_threads_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.endpoint, self.token)

        list_chat_threads_result = None
        async with chat_client:
            try:
                list_chat_threads_result = await chat_client.list_threads()
            except HttpResponseError as e:
                print(e)
                return

        print("list_chat_threads succeeded, count of chat threads: ", len(list_chat_threads_result.threads))

    async def update_thread_async(self):
        from azure.core.exceptions import HttpResponseError

        try:
            topic = "update topic"
            await self._chat_thread_client.update_thread(topic=topic)
        except HttpResponseError as e:
            print(e)
            return

        print("update_thread succeeded")

    async def delete_thread_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.endpoint, self.token)

        async with chat_client:
            try:
                await chat_client.delete_thread(self._thread_id)
            except HttpResponseError as e:
                print(e)
                return

        print("delete_thread succeeded")

    async def send_message_async(self):
        from azure.communication.chat.models import ChatMessagePriorityDto
        from azure.core.exceptions import HttpResponseError

        send_message_result = None
        try:
            priority=ChatMessagePriorityDto.NORMAL
            content='hello world'
            sender_display_name='sender name'

            send_message_result = await self._chat_thread_client.send_message(
                content,
                priority=priority,
                sender_display_name=sender_display_name)
        except HttpResponseError as e:
            print(e)
            return

        self._message_id = send_message_result.id
        print("send_message succeeded, message id:", self._message_id)

    async def get_message_async(self):
        from azure.core.exceptions import HttpResponseError

        chat_message = None
        try:
            chat_message = await self._chat_thread_client.get_message(self._message_id)
        except HttpResponseError as e:
            print(e)
            return

        print("get_message succeeded, message id:", chat_message.id, \
            "content: ", chat_message.content)

    async def list_messages_async(self):
        from azure.core.exceptions import HttpResponseError

        list_chat_messages_result = None
        try:
            list_chat_messages_result = await self._chat_thread_client.list_messages()
        except HttpResponseError as e:
            print(e)
            return

        print("list_messages succeeded, messages count:",
            len([elem for elem in list_chat_messages_result.messages if elem.type == 'Text']))

    async def update_message_async(self):
        from azure.core.exceptions import HttpResponseError

        try:
            content = "updated message content"
            await self._chat_thread_client.update_message(self._message_id, content=content)
        except HttpResponseError as e:
            print(e)
            return

        print("update_message succeeded")

    async def send_read_receipt_async(self):
        from azure.core.exceptions import HttpResponseError

        try:
            await self._chat_thread_client.send_read_receipt(self._message_id)
        except HttpResponseError as e:
            print(e)
            return

        print("send_read_receipt succeeded")

    async def list_read_receipts_async(self):
        from azure.core.exceptions import HttpResponseError

        read_receipts = []
        try:
            read_receipts = await self._chat_thread_client.list_read_receipts()
        except HttpResponseError as e:
            print(e)
            return

        print("list_read_receipts succeeded, receipts:")
        for read_receipt in read_receipts:
            print(read_receipt)

    async def delete_message_async(self):
        from azure.core.exceptions import HttpResponseError

        try:
            await self._chat_thread_client.delete_message(self._message_id)
        except HttpResponseError as e:
            print(e)
            return

        print("delete_message succeeded")

    async def list_members_async(self):
        from azure.core.exceptions import HttpResponseError

        chat_thread_members = []
        try:
            chat_thread_members = await self._chat_thread_client.list_members()
        except HttpResponseError as e:
            print(e)
            return

        print("list_members succeeded, members:")
        for member in chat_thread_members:
            print(member)

    async def add_members_async(self):
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
        members = [new_member]

        try:
            await self._chat_thread_client.add_members(members)
        except HttpResponseError as e:
            print(e)
            return

        print("add_members succeeded")

    async def remove_member_async(self):
        from azure.core.exceptions import HttpResponseError

        # this member was added when calling add_members()
        added_member_id = \
            self._thread_creator[:self._thread_creator.rfind("_")] + "_" \
            + "123456-0000123456"

        try:
            await self._chat_thread_client.remove_member(added_member_id)
        except HttpResponseError as e:
            print(e)
            return

        print("remove_member_async succeeded")

    async def send_typing_notification_async(self):
        from azure.core.exceptions import HttpResponseError

        try:
            await self._chat_thread_client.send_typing_notification()
        except HttpResponseError as e:
            print(e)
            return

        print("send_typing_notification succeeded")

async def main():
    sample = ChatSamplesAsync()
    await sample.create_thread_async()
    await sample.update_thread_async()
    await sample.get_thread_async()
    await sample.list_threads_async()
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
    await sample._chat_thread_client.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())