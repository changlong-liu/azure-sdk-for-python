# ------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -------------------------------------------------------------------------

import base64
import json
import datetime
from typing import (  # pylint: disable=unused-import
    cast,
    Tuple,
)
from datetime import datetime
from azure.core.credentials import AccessToken

def parse_connection_str(conn_str):
    # type: (str) -> Tuple[str, str, str, str]
    endpoint = None
    shared_access_key = None
    for element in conn_str.split(";"):
        key, _, value = element.partition("=")
        if key.lower() == "endpoint":
            endpoint = value.rstrip("/")
        elif key.lower() == "accesskey":
            shared_access_key = value
    if not all([endpoint, shared_access_key]):
        raise ValueError(
            "Invalid connection string. Should be in the format: "
            "endpoint=sb://<FQDN>/;accesskey=<KeyValue>"
        )
    left_slash_pos = cast(str, endpoint).find("//")
    if left_slash_pos != -1:
        host = cast(str, endpoint)[left_slash_pos + 2:]
    else:
        host = str(endpoint)

    return host, str(shared_access_key)


def get_current_utc_time():
    # type: () -> str
    return str(datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S ")) + "GMT"

def create_access_token(token):
    # type: (str) -> azure.core.credentials.AccessToken
    """Creates an instance of azure.core.credentials.AccessToken from a
    string token.

    :param token: User token
    :type token: str
    :return: Instance of azure.core.credentials.AccessToken - token and expiry date of it
    :rtype: ~azure.core.credentials.AccessToken
    """

    token_parse_err_msg = "Token is not formatted correctly"
    parts = token.split(".")

    if len(parts) < 3:
        raise ValueError(token_parse_err_msg)

    try:
        payload_str = base64.b64decode(parts[1].
            replace('-', '+').
            replace('_', '-') + "="*(4-len(parts[1])%4))

        payload = json.loads(payload_str)
        return AccessToken(token, datetime.fromtimestamp(payload['exp']))
    except ValueError:
        raise ValueError(token_parse_err_msg)
