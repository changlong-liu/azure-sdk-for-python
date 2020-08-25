# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE.txt in the project root for
# license information.
# -------------------------------------------------------------------------
from azure.communication.chat.aio import ChatClient
from azure.communication.chat import ChatThreadMember
from helpers import mock_response
from azure.core.exceptions import HttpResponseError

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

@pytest.mark.asyncio
async def test_create_thread_raises_error():
    async def mock_send(*_, **__):
        return mock_response(status_code=400, json_payload={"msg": "some error"})
    chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

    topic="test topic",
    thread_members=[ChatThreadMember(
        id='8:acs:57b9bac9-df6c-4d39-a73b-26e944adf6ea_9b0110-08007f1041',
        display_name='name',
        share_history_time='0'
    )]

    raised = False
    try:
        await chat_client.create_thread(topic=topic, thread_members=thread_members)
    except:
        raised = True

    assert raised == True

@pytest.mark.asyncio
async def test_delete_thread():
    thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
    raised = False

    async def mock_send(*_, **__):
        return mock_response(status_code=204)
    chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

    raised = False
    try:
        await chat_client.delete_thread(thread_id)
    except:
        raised = True

    assert raised == False

@pytest.mark.asyncio
async def test_get_thread():
    thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
    raised = False

    async def mock_send(*_, **__):
        return mock_response(status_code=200, json_payload={"id": thread_id})
    chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

    get_thread_result = None
    try:
        get_thread_result = await chat_client.get_thread(thread_id)
    except:
        raised = True

    assert raised == False
    assert get_thread_result.id == thread_id

@pytest.mark.asyncio
async def test_list_threads():
    thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
    raised = False

    async def mock_send(*_, **__):
        return mock_response(status_code=200, json_payload={"value": [{"id": thread_id}]})
    chat_client = ChatClient("some_token", "https://endpoint", transport=Mock(send=mock_send))

    chat_thread_infos = None
    try:
        chat_thread_infos = chat_client.list_threads()
    except:
        raised = True

    assert raised == False
    async for chat_thread_page in chat_thread_infos.by_page():
        l = [ i async for i in chat_thread_page]
        assert len(l) == 1
        assert l[0].id == thread_id

def test_get_thread_client():
    thread_id = "19:bcaebfba0d314c2aa3e920d38fa3df08@thread.v2"
    chat_client = ChatClient("some_token", "https://endpoint")
    chat_thread_client = chat_client.get_chat_thread_client(thread_id)

    assert chat_thread_client.thread_id == thread_id