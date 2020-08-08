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

    def test_create_thread(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        create_thread_response = None
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=201, json_payload={"id": thread_id})
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        create_thread_request = CreateThreadRequest(
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
            create_thread_response = chat_client.create_thread(create_thread_request)
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')
        assert create_thread_response.id == thread_id

    def test_create_thread_raises_error(self):
        def mock_send(*_, **__):
            return mock_response(status_code=400, json_payload={"msg": "some error"})
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        create_thread_request = CreateThreadRequest(
                topic="test topic",
                members=[ThreadMember(
                    id='8:spool:57b9bac9-df6c-4d39-a73b-26e944adf6ea_9b0110-08007f1041',
                    display_name='name',
                    member_role='Admin',
                    share_history_time='0'
                )],
                is_sticky_thread=False
            )

        self.assertRaises(HttpResponseError, chat_client.create_thread, create_thread_request=create_thread_request)

    def test_update_thread(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=200)
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        update_thread_request = UpdateThreadRequest(topic="update topic")
        try:
            chat_client.update_thread(thread_id, update_thread_request)
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')

    def test_delete_thread(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=200)
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        try:
            chat_client.delete_thread(thread_id)
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')

    def test_send_message(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        client_message_id='1581637626706'
        message_id='1596823919339'
        raised = False

        def mock_send(*_, **__):
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
            create_message_response = chat_client.send_message(thread_id, create_message_request)
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')
        assert create_message_response.id == message_id

    def test_get_message(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        message_id='1596823919339'
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=200, json_payload={"id": message_id})
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        message = None
        try:
            message = chat_client.get_message(thread_id, message_id)
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')
        assert message.id == message_id

    def test_list_messages(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        message_id='1596823919339'
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=200, json_payload={"messages": [{"id": message_id}]})
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        list_messages_response = None
        try:
            list_messages_response = chat_client.list_messages(thread_id)
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')
        assert len(list_messages_response.messages) == 1
        assert list_messages_response.messages[0].id == message_id

    def test_udpate_message(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        message_id='1596823919339'
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=200)
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        try:
            update_message_request = UpdateMessageRequest(content="updated message content")
            chat_client.update_message(thread_id, message_id, update_message_request)
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')

    def test_delete_message(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        message_id='1596823919339'
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=200)
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        try:
            chat_client.delete_message(thread_id, message_id)
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')

if __name__ == '__main__':
    unittest.main()