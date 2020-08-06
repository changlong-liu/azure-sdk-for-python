# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: configuration_sample_usertoken_issue.py
DESCRIPTION:
    These samples demonstrate user token management operations.
    
    ///authenticating a client via a connection string
USAGE:
    python configuration_sample_usertoken_issue.py
"""

import sys
sys.path.append("..")

class UserTokenSamples(object):

    def auth_connection_string(self):
        connection_string = "[CONNECTION-STRING]"
        from azure.communication.configuration._user_management_client import UserManagementClient

        user_token_client = UserManagementClient.from_connection_string(connection_string)
        tokenresponse = user_token_client.user_management.issue_token(scopes=["chat"])
        print(tokenresponse)
        # [END auth_from_connection_string]


if __name__ == '__main__':
    sample = UserTokenSamples()
    sample.auth_connection_string()