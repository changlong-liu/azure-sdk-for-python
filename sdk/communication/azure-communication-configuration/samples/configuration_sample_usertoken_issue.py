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
        connection_string = "endpoint=https://tufarhad-r.eastus.dev.communications.azure.net/;accesskey=eLMSrNfwXbl6ewOO5/+Dn2Nbs1hzYLYFUE/uq/RJZlb8b0iKNW4nimlVnITlWIcDq4Juu0P1JKWyL+3NN0TQfA=="
        from azure.communication.configuration._user_token_client import UserTokenClient

        user_token_client = UserTokenClient.from_connection_string(connection_string)
        tokenresponse = user_token_client.user_management.issue_token(scopes=["chat"])
        print(tokenresponse)
        # [END auth_from_connection_string]


if __name__ == '__main__':
    sample = UserTokenSamples()
    sample.auth_connection_string()