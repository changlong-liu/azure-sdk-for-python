# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import unittest

from azure.core.exceptions import HttpResponseError
from azure.communication.chat import ChatClient
from azure.communication.chat import ChatThreadMember
from helpers import mock_response
from datetime import datetime

try:
    from unittest.mock import Mock, patch
except ImportError:  # python < 3.3
    from mock import Mock, patch  # type: ignore


class TestChatClient(unittest.TestCase):

    def test_create_thread(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        chat_thread_client = None
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=201, json_payload={"id": thread_id})
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        topic="test topic"
        members=[ChatThreadMember(
            id='8:acs:57b9bac9-df6c-4d39-a73b-26e944adf6ea_9b0110-08007f1041',
            display_name='name',
            share_history_time=datetime.utcnow()
        )]
        try:
            chat_thread_client = chat_client.create_chat_thread(topic, members)
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')
        assert chat_thread_client.thread_id == thread_id

    def test_create_thread_raises_error(self):
        def mock_send(*_, **__):
            return mock_response(status_code=400, json_payload={"msg": "some error"})
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        topic="test topic",
        thread_members=[ChatThreadMember(
            id='8:acs:57b9bac9-df6c-4d39-a73b-26e944adf6ea_9b0110-08007f1041',
            display_name='name',
            share_history_time=datetime.utcnow()
        )]

        self.assertRaises(HttpResponseError, chat_client.create_chat_thread, topic=topic, thread_members=thread_members)

    def test_delete_thread(self):
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

    def test_get_thread(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=200, json_payload={"id": thread_id})
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        get_thread_result = None
        try:
            get_thread_result = chat_client.get_chat_thread(thread_id)
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')
        assert get_thread_result.id == thread_id

    def test_list_threads(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=200, json_payload={"value": [{"id": thread_id}]})
        chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

        chat_thread_infos = None
        try:
            chat_thread_infos = chat_client.list_chat_threads()
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')
        for chat_thread_page in chat_thread_infos.by_page():
            l = list(chat_thread_page)
            assert len(l) == 1
            assert l[0].id == thread_id

    def test_get_thread_client(self):
        thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        chat_client = ChatClient("some_token", "https://endpoint")
        chat_thread_client = chat_client.get_chat_thread_client(thread_id)

        assert chat_thread_client.thread_id == thread_id

if __name__ == '__main__':
    unittest.main()