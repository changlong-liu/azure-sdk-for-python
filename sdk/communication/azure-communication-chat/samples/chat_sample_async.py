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

    ///use ChatClient to perform a chatting sencario, like
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
    skype_token = os.environ.get("SKYPE_TOKEN", None)
    if not skype_token:
        raise ValueError("Set SKYPE_TOKEN env before run this sample.")

    _thread_id = None
    _thread_creator = None
    _message_id = None
    _client_message_id = None

    async def create_thread_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.communication.chat.models import CreateThreadRequest, ThreadMember

        chat_client = ChatClient(self.skype_token, self.endpoint)

        # the user who makes the request must be in the member list of the CreateThreadRequest
        user_id = "8:" + jwt.decode(self.skype_token, verify=False)['skypeid']
        self._thread_creator = user_id

        create_thread_response = None
        async with chat_client:
            try:
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
                create_thread_response = await chat_client.create_thread(body)

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
                thread = await chat_client.get_thread(self._thread_id)
            except HttpResponseError as e:
                print(e)
                return

        print("get_thread succeded, thread id: " + thread.id + ", thread topic: " + thread.topic)

    async def update_thread_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.communication.chat.models import UpdateThreadRequest
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)

        async with chat_client:
            try:
                update_thread_request = UpdateThreadRequest(topic="update topic")
                await chat_client.update_thread(self._thread_id, update_thread_request)
            except HttpResponseError as e:
                print(e)
                return

        print("update_thread succeded")

    async def delete_thread_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)

        async with chat_client:
            try:
                await chat_client.delete_thread(self._thread_id)
            except HttpResponseError as e:
                print(e)
                return

        print("delete_thread succeded")

    async def send_message_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.communication.chat.models import CreateMessageRequest, MessagePriority
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)
        create_message_response = None

        async with chat_client:
            try:
                create_message_request = CreateMessageRequest(
                    client_message_id='1581637626706',
                    priority=MessagePriority.NORMAL,
                    content='hello world',
                    sender_display_name='sender name',
                )
                create_message_response = await chat_client.send_message(
                    self._thread_id,
                    create_message_request)
            except HttpResponseError as e:
                print(e)
                return

        self._message_id = create_message_response.id
        self._client_message_id = create_message_response.client_message_id
        print("send_message succeded, message id:", self._message_id)

    async def get_message_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)
        message = None

        async with chat_client:
            try:
                message = await chat_client.get_message(self._thread_id, self._message_id)
            except HttpResponseError as e:
                print(e)
                return

        print("get_message succeded, message id:", message.id)

    async def list_messages_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)
        list_messages_response = None

        async with chat_client:
            try:
                list_messages_response = await chat_client.list_messages(self._thread_id)
            except HttpResponseError as e:
                print(e)
                return

        print("list_messages succeded, messages count:",
            len([elem for elem in list_messages_response.messages if elem.message_type == 'Text']))

    async def update_message_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.communication.chat.models import UpdateMessageRequest
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)

        async with chat_client:
            try:
                update_message_request = UpdateMessageRequest(content="updated message content")
                await chat_client.update_message(self._thread_id, self._message_id, update_message_request)
            except HttpResponseError as e:
                print(e)
                return

        print("update_message succeded")

    async def delete_message_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)

        async with chat_client:
            try:
                await chat_client.delete_message(self._thread_id, self._message_id)
            except HttpResponseError as e:
                print(e)
                return

        print("delete_message succeded")

    async def list_members_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)

        members = []
        async with chat_client:
            try:
                members = await chat_client.list_members(self._thread_id)
            except HttpResponseError as e:
                print(e)
                return

        print("list_members succeded, members:")
        for member in members:
            print(member)

    async def add_members_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.communication.chat.models import AddThreadMembersRequest, ThreadMember
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)

        # the new member must has the same resource id as the thread creator
        new_member_id = \
            self._thread_creator[:self._thread_creator.rfind("_")] + "_" \
            + "123456-0000123456"
        new_member = ThreadMember(
                id=new_member_id,
                display_name='name',
                member_role='Admin',
                share_history_time='0')
        add_thread_members_request = AddThreadMembersRequest(members=[new_member])

        async with chat_client:
            try:
                await chat_client.add_members(self._thread_id, add_thread_members_request)
            except HttpResponseError as e:
                print(e)
                return

        print("add_members succeded")

    async def remove_member_async(self):
        from azure.communication.chat.aio import ChatClient
        from azure.communication.chat.models import AddThreadMembersRequest, ThreadMember
        from azure.core.exceptions import HttpResponseError

        chat_client = ChatClient(self.skype_token, self.endpoint)

        # this member was added when calling add_members()
        added_member_id = \
            self._thread_creator[:self._thread_creator.rfind("_")] + "_" \
            + "123456-0000123456"

        async with chat_client:
            try:
                await chat_client.remove_member(self._thread_id, added_member_id)
            except HttpResponseError as e:
                print(e)
                return

        print("remove_member_async succeded")

async def main():
    sample = ChatSamplesAsync()
    await sample.create_thread_async()
    await sample.get_thread_async()
    await sample.update_thread_async()
    await sample.send_message_async()
    await sample.get_message_async()
    await sample.list_messages_async()
    await sample.update_message_async()
    await sample.delete_message_async()
    await sample.list_members_async()
    await sample.add_members_async()
    await sample.remove_member_async()
    await sample.delete_thread_async()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())