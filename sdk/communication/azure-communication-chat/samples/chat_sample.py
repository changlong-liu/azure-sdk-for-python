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

import sys
sys.path.append("..")


class ChatSamples(object):
    def create_client(self):
        skypetoken = "[skypetoken]"
        host = "https://acs-chat-e2e.eastus.dev.communications.azure.net"
        from azure.communication.chat._chat_client import ChatClient
        chat_client = ChatClient(host, skypetoken)


if __name__ == '__main__':
    sample = ChatSamples()
    sample.create_thread()
