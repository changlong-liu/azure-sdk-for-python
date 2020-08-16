# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import unittest

from azure.core.exceptions import HttpResponseError
from azure.communication.chat import ChatClient
from azure.communication.chat.models import *
from helpers import mock_response

try:
    from unittest.mock import Mock, patch
except ImportError:  # python < 3.3
    from mock import Mock, patch  # type: ignore


class TestChatClient(unittest.TestCase):

    def test_create_chat_thread(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        create_thread_result = None
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=201, json_payload={"id": thread_id})
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        topic="test topic"
        members=[ThreadMember(
            id='8:spool:57b9bac9-df6c-4d39-a73b-26e944adf6ea_9b0110-08007f1041',
            display_name='name',
            share_history_time='0'
        )]
        try:
            create_thread_result = chat_client.create_chat_thread(topic, members)
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')
        assert create_thread_result.id == thread_id

    def test_create_chat_thread_raises_error(self):
        def mock_send(*_, **__):
            return mock_response(status_code=400, json_payload={"msg": "some error"})
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        topic="test topic",
        members=[ThreadMember(
            id='8:spool:57b9bac9-df6c-4d39-a73b-26e944adf6ea_9b0110-08007f1041',
            display_name='name',
            share_history_time='0'
        )]

        self.assertRaises(HttpResponseError, chat_client.create_chat_thread, topic=topic, members=members)

    def test_update_chat_thread(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=200)
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        topic = "update topic"
        try:
            chat_client.update_chat_thread(thread_id, topic)
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')

    def test_delete_chat_thread(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=204)
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        try:
            chat_client.delete_chat_thread(thread_id)
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')

    def test_send_chat_message(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        message_id='1596823919339'
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=201, json_payload={"id": message_id})
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        create_message_result = None
        try:
            priority=MessagePriority.NORMAL
            content='hello world'
            sender_display_name='sender name'

            create_message_result = chat_client.send_chat_message(
                thread_id,
                content,
                priority=priority,
                sender_display_name=sender_display_name)
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')
        assert create_message_result.id == message_id

    def test_get_chat_message(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        message_id='1596823919339'
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=200, json_payload={"id": message_id})
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        message = None
        try:
            message = chat_client.get_chat_message(thread_id, message_id)
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')
        assert message.id == message_id

    def test_list_chat_messages(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        message_id='1596823919339'
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=200, json_payload={"messages": [{"id": message_id}]})
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        list_messages_response = None
        try:
            list_messages_response = chat_client.list_chat_messages(thread_id)
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')
        assert len(list_messages_response.messages) == 1
        assert list_messages_response.messages[0].id == message_id

    def test_update_chat_message(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        message_id='1596823919339'
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=200)
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        try:
            content = "updated message content"
            chat_client.update_chat_message(thread_id, message_id, content)
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')

    def test_delete_chat_message(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        message_id='1596823919339'
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=200)
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        try:
            chat_client.delete_chat_message(thread_id, message_id)
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')

    def test_list_chat_members(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        member_id="8:acs:57b9bac9-df6c-4d39-a73b-26e944adf6ea_9b0110-08007f1041"
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=200, json_payload=[{"id": member_id}])
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        try:
            members = chat_client.list_chat_members(thread_id)
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')
        assert len(members) == 1
        assert members[0].id == member_id

    def test_add_chat_members(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        new_member_id="8:acs:57b9bac9-df6c-4d39-a73b-26e944adf6ea_9b0110-08007f1041"
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=201)
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        new_member = ThreadMember(
                id=new_member_id,
                display_name='name',
                share_history_time='0')
        members = [new_member]

        try:
            chat_client.add_chat_members(thread_id, members)
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')

    def test_remove_chat_member(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        member_id="8:acs:57b9bac9-df6c-4d39-a73b-26e944adf6ea_9b0110-08007f1041"
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=200)
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        try:
            chat_client.remove_chat_member(thread_id, member_id)
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')

    def test_send_typing_notification(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=200)
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        try:
            chat_client.send_typing_notification(thread_id)
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')

    def test_send_read_receipt(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        message_id='1596823919339'
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=201)
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        try:
            chat_client.send_read_receipt(thread_id, message_id)
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')

if __name__ == '__main__':
    unittest.main()