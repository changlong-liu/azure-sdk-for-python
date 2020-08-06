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
        expected_thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
        create_thread_response = None
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=201, json_payload={"id": expected_thread_id})
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
            create_thread_response = chat_client.create_thread(body)
        except:
            raised = True

        self.assertFalse(raised, 'Expected is no excpetion raised')
        assert create_thread_response.id == expected_thread_id

    def test_create_thread_raises_error(self):
        expected_thread_id = None
        create_thread_response = None
        raised = False

        def mock_send(*_, **__):
            return mock_response(status_code=400, json_payload={"msg": "some error"})
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
        
        self.assertRaises(HttpResponseError, chat_client.create_thread, body=body)

if __name__ == '__main__':
    unittest.main()