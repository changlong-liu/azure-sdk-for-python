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

from azure.communication.chat._generated import models
import os
#import sys
#sys.path.append("..")


class ChatSamples(object):

    url = os.environ.get("AZURE_COMMUNICATION_SERVICE_ENDPOINT", None)
    if not url:
        raise ValueError("Set AZURE_COMMUNICATION_SERVICE_ENDPOINT env before run this sample.")
    skype_token = os.environ.get("SKYPE_TOKEN", None)
    if not skype_token:
        raise ValueError("Set SKYPE_TOKEN env before run this sample.")

    def create_client(self):
        skypetoken = "[skypetoken]"
        host = "https://acs-chat-e2e.eastus.dev.communications.azure.net"
        from azure.communication.chat._chat_client import ChatClient
        chat_client = ChatClient(host, skypetoken)

    def create_thread(self):
        from azure.communication.chat._chat_client import ChatClient
        chat_client = ChatClient(self.url, self.skype_token)
        topic = "test topic"
        is_sticky_thread = False
        member = models.ThreadMember(
            id='8:spool:57b9bac9-df6c-4d39-a73b-26e944adf6ea_9b0110-08007f1041',
            display_name='name',
            member_role='Admin',
            share_history_time='0')
        members = [member]
        thread = chat_client.create_thread(topic, members, is_sticky_thread)
        print("thread created, id: " + thread.id)

if __name__ == '__main__':
    sample = ChatSamples()
    sample.create_thread()