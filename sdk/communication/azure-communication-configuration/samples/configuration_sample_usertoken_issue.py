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
    
    ///authenticating a client via a connection string,
    shared access key, or by generating a sas token with which the returned signature
    can be used with the credential parameter of any BlobServiceClient,
    ContainerClient, BlobClient.///
USAGE:
    python configuration_sample_usertoken_issue.py
"""

import sys
sys.path.append("..")

class UserTokenSamples(object):

    def auth_connection_string(self):
        connection_string = "[CONNECTION-STRING]"
        from azure.communication._user_token_client import UserTokenClient

        user_token_client = UserTokenClient.from_connection_string(connection_string)
        tokenresponse = user_token_client.issue("tural@contoso.com", scopes=["chat"])
        print(tokenresponse)
        # [END auth_from_connection_string]


if __name__ == '__main__':
    sample = UserTokenSamples()
    sample.auth_connection_string()