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

    async def create_thread_async(self):
        from azure.communication.chat.aio._chat_client_async import ChatClient
        from azure.communication.chat._generated import models
        
        chat_client = ChatClient(self.skype_token, self.endpoint)
        
        # the user who makes the request must be in the member list of the CreateThreadRequest
        user_id = "8:" + jwt.decode(self.skype_token, verify=False)['skypeid']

        async with chat_client:
            try:
                body = models.CreateThreadRequest(
                    topic="test topic",
                    members=[models.ThreadMember(
                        id=user_id,
                        display_name='name',
                        member_role='Admin',
                        share_history_time='0'
                    )],
                    is_sticky_thread=False
                )
                thread = await chat_client.create_thread(body)
                print("thread created, id: " + thread.id)
            finally:
                return

async def main():
    sample = ChatSamplesAsync()
    await sample.create_thread_async()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())