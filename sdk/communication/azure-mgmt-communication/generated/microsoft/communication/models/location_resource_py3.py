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


class LocationResource(Model):
    """An ARM resource with its own location (not a global or an inherited
    location).

    :param location: The Azure location where the CommunicationService is
     running.
    :type location: str
    """

    _attribute_map = {
        'location': {'key': 'location', 'type': 'str'},
    }

    def __init__(self, *, location: str=None, **kwargs) -> None:
        super(LocationResource, self).__init__(**kwargs)
        self.location = location
