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

from msrest.paging import Paged


class OperationPaged(Paged):
    """
    A paging container for iterating over a list of :class:`Operation <azure.mgmt.machinelearningservices.models.Operation>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[Operation]'}
    }

    def __init__(self, *args, **kwargs):

        super(OperationPaged, self).__init__(*args, **kwargs)
class WorkspacePaged(Paged):
    """
    A paging container for iterating over a list of :class:`Workspace <azure.mgmt.machinelearningservices.models.Workspace>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[Workspace]'}
    }

    def __init__(self, *args, **kwargs):

        super(WorkspacePaged, self).__init__(*args, **kwargs)
class ComputeResourcePaged(Paged):
    """
    A paging container for iterating over a list of :class:`ComputeResource <azure.mgmt.machinelearningservices.models.ComputeResource>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[ComputeResource]'}
    }

    def __init__(self, *args, **kwargs):

        super(ComputeResourcePaged, self).__init__(*args, **kwargs)
