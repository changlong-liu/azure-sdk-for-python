# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import asyncio
import unittest

from azure.core.exceptions import HttpResponseError
from azure.communication.chat.aio import ChatClient
from azure.communication.chat.models import *
from helpers import mock_response

try:
    from unittest.mock import Mock, patch
except ImportError:  # python < 3.3
    from mock import Mock, patch  # type: ignore


class TestChatClientAsync(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def test_create_thread_async(self):
        async def go():
            thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
            create_thread_response = None
            raised = False

            async def mock_send(*_, **__):
                return mock_response(status_code=201, json_payload={"id": thread_id})
            chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

            body = CreateThreadRequest(
                    topic="test topic",
                    members=[ThreadMember(
                        id='8:spool:57b9bac9-df6c-4d39-a73b-26e944adf6ea_9b0110-08007f1041',
                        display_name='name',
                        member_role='Admin',
                        share_history_time='0'
                    )],
                    is_sticky_thread=False
                )
            try:
                create_thread_response = await chat_client.create_thread(body)
            except:
                raised = True

            self.assertFalse(raised, 'Expected is no excpetion raised')
            assert create_thread_response.id == thread_id

        self.loop.run_until_complete(go())

    def test_create_thread_raises_error(self):
        async def go():
            create_thread_response = None
            raised = False

            async def mock_send(*_, **__):
                return mock_response(status_code=400, json_payload={"msg": "some error"})
            chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

            body = CreateThreadRequest(
                    topic="test topic",
                    members=[ThreadMember(
                        id='8:acs:57b9bac9-df6c-4d39-a73b-26e944adf6ea_9b0110-08007f1041',
                        display_name='name',
                        member_role='Admin',
                        share_history_time='0'
                    )],
                    is_sticky_thread=False
                )

            try:
                create_thread_response = await chat_client.create_thread(body)
            except HttpResponseError:
                raised = True
            self.assertTrue(raised, 'HttpResponseError is expected')

        self.loop.run_until_complete(go())

    def test_update_thread_async(self):
        async def go():
            raised = False
            thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"

            async def mock_send(*_, **__):
                return mock_response(status_code=200)
            chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

            update_thread_request = UpdateThreadRequest(topic="updated topic")

            try:
                await chat_client.update_thread(thread_id, update_thread_request)
            except:
                raised = True
            self.assertFalse(raised, 'Expected is no excpetion raised')

        self.loop.run_until_complete(go())

    def test_delete_thread_async(self):
        async def go():
            raised = False
            thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"

            async def mock_send(*_, **__):
                return mock_response(status_code=200)
            chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

            try:
                await chat_client.delete_thread(thread_id)
            except:
                raised = True
            self.assertFalse(raised, 'Expected is no excpetion raised')

        self.loop.run_until_complete(go())

    def tets_send_message_async(self):
        async def go():
            raised = False
            thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
            client_message_id='1581637626706'
            message_id='1596823919339'

            async def mock_send(*_, **__):
                return mock_response(status_code=201, json_payload={"id": message_id})
            chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

            create_message_response = None
            try:
                create_message_request = CreateMessageRequest(
                    client_message_id=client_message_id,
                    priority=MessagePriority.NORMAL,
                    content='hello world',
                    sender_display_name='sender name',
                )
                create_message_response = await chat_client.send_message(thread_id, create_message_request)
            except:
                raised = True

            self.assertFalse(raised, 'Expected is no excpetion raised')
            assert create_message_response.id == message_id

        self.loop.run_until_complete(go())

    def test_get_message_async(self):
        async def go():
            thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
            message_id='1596823919339'
            raised = False

            async def mock_send(*_, **__):
                return mock_response(status_code=200, json_payload={"id": message_id})
            chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

            message = None
            try:
                message = await chat_client.get_message(thread_id, message_id)
            except:
                raised = True

            self.assertFalse(raised, 'Expected is no excpetion raised')
            assert message.id == message_id

        self.loop.run_until_complete(go())

    def test_list_messages_async(self):
        async def go():
            thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
            message_id='1596823919339'
            raised = False

            async def mock_send(*_, **__):
                return mock_response(status_code=200, json_payload={"messages": [{"id": message_id}]})
            chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

            list_messages_response = None
            try:
                list_messages_response = await chat_client.list_messages(thread_id)
            except:
                raised = True

            self.assertFalse(raised, 'Expected is no excpetion raised')
            assert len(list_messages_response.messages) == 1
            assert list_messages_response.messages[0].id == message_id

        self.loop.run_until_complete(go())

    def test_delete_message_async(self):
        async def go():
            thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
            message_id='1596823919339'
            raised = False

            async def mock_send(*_, **__):
                return mock_response(status_code=200)
            chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

            try:
                await chat_client.delete_message(thread_id, message_id)
            except:
                raised = True

            self.assertFalse(raised, 'Expected is no excpetion raised')

        self.loop.run_until_complete(go())

    def test_list_members_async(self):
        async def go():
            thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
            member_id="8:acs:57b9bac9-df6c-4d39-a73b-26e944adf6ea_9b0110-08007f1041"
            raised = False

            async def mock_send(*_, **__):
                return mock_response(status_code=200, json_payload=[{"id": member_id}])
            chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

            members = []
            try:
                members = await chat_client.list_members(thread_id)
            except:
                raised = True

            self.assertFalse(raised, 'Expected is no excpetion raised')
            assert len(members) == 1
            assert members[0].id == member_id

        self.loop.run_until_complete(go())

    def test_add_members_async(self):
        async def go():
            thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
            new_member_id="8:acs:57b9bac9-df6c-4d39-a73b-26e944adf6ea_9b0110-08007f1041"
            raised = False

            async def mock_send(*_, **__):
                return mock_response(status_code=201)
            chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

            new_member = ThreadMember(
                id=new_member_id,
                display_name='name',
                member_role='Admin',
                share_history_time='0')
            add_thread_members_request = AddThreadMembersRequest(members=[new_member])
            try:
                await chat_client.add_members(thread_id, add_thread_members_request)
            except:
                raised = True

            self.assertFalse(raised, 'Expected is no excpetion raised')

        self.loop.run_until_complete(go())

    def test_remove_member_async(self):
        async def go():
            thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
            member_id="8:acs:57b9bac9-df6c-4d39-a73b-26e944adf6ea_9b0110-08007f1041"
            raised = False

            async def mock_send(*_, **__):
                return mock_response(status_code=200)
            chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

            try:
                await chat_client.remove_member(thread_id, member_id)
            except:
                raised = True

            self.assertFalse(raised, 'Expected is no excpetion raised')

        self.loop.run_until_complete(go())

    def tearDown(self):
        self.loop.close()

if __name__ == '__main__':
    unittest.main()