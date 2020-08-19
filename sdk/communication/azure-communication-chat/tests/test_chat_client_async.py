# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE.txt in the project root for
# license information.
# -------------------------------------------------------------------------
from azure.communication.chat.aio import ChatClient
from azure.communication.chat.models import ChatThreadMember
from helpers import mock_response

try:
    from unittest.mock import Mock, patch
except ImportError:  # python < 3.3
    from mock import Mock, patch  # type: ignore

import pytest

@pytest.mark.asyncio
async def test_create_thread():
    thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"

    async def mock_send(*_, **__):
        return mock_response(status_code=201, json_payload={"id": thread_id})

    chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

    topic="test topic"
    members=[ChatThreadMember(
        id='8:acs:57b9bac9-df6c-4d39-a73b-26e944adf6ea_9b0110-08007f1041',
        display_name='name',
        share_history_time='0'
    )]
    chat_thread_client = await chat_client.create_thread(topic, members)
    assert chat_thread_client.thread_id == thread_id