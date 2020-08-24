# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ApnsCredential(Model):
    """Credentials for pushing through APNS.

    All required parameters must be populated in order to send to Azure.

    :param endpoint: Required. The endpoint of this credential. Possible
     values include: 'Development', 'Production'
    :type endpoint: str or ~microsoft.communication.models.Endpoint
    :param token: Required. Provider Authentication Token, obtained through
     your developer account
    :type token: str
    :param key_id: Required. A 10-character key identifier (kid) key, obtained
     from your developer account.
    :type key_id: str
    :param bundle_id: Required. The name of the application or BundleId.
    :type bundle_id: str
    :param team_id: Required. A 10 character TeamId, also referred to as the
     App ID Prefix, obtained from your developer account.
    :type team_id: str
    """

    _validation = {
        'endpoint': {'required': True},
        'token': {'required': True},
        'key_id': {'required': True},
        'bundle_id': {'required': True},
        'team_id': {'required': True},
    }

    _attribute_map = {
        'endpoint': {'key': 'endpoint', 'type': 'Endpoint'},
        'token': {'key': 'token', 'type': 'str'},
        'key_id': {'key': 'keyId', 'type': 'str'},
        'bundle_id': {'key': 'bundleId', 'type': 'str'},
        'team_id': {'key': 'teamId', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(ApnsCredential, self).__init__(**kwargs)
        self.endpoint = kwargs.get('endpoint', None)
        self.token = kwargs.get('token', None)
        self.key_id = kwargs.get('key_id', None)
        self.bundle_id = kwargs.get('bundle_id', None)
        self.team_id = kwargs.get('team_id', None)
