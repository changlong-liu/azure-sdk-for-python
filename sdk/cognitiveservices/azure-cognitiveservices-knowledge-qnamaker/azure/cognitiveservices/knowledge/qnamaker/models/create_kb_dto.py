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


class CreateKbDTO(Model):
    """Post body schema for CreateKb operation.

    All required parameters must be populated in order to send to Azure.

    :param name: Required. Friendly name for the knowledgebase.
    :type name: str
    :param qna_list: List of Q-A (QnADTO) to be added to the knowledgebase.
     Q-A Ids are assigned by the service and should be omitted.
    :type qna_list:
     list[~azure.cognitiveservices.knowledge.qnamaker.models.QnADTO]
    :param urls: List of URLs to be used for extracting Q-A.
    :type urls: list[str]
    :param files: List of files from which to Extract Q-A.
    :type files:
     list[~azure.cognitiveservices.knowledge.qnamaker.models.FileDTO]
    """

    _validation = {
        'name': {'required': True, 'max_length': 100, 'min_length': 1},
    }

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'qna_list': {'key': 'qnaList', 'type': '[QnADTO]'},
        'urls': {'key': 'urls', 'type': '[str]'},
        'files': {'key': 'files', 'type': '[FileDTO]'},
    }

    def __init__(self, **kwargs):
        super(CreateKbDTO, self).__init__(**kwargs)
        self.name = kwargs.get('name', None)
        self.qna_list = kwargs.get('qna_list', None)
        self.urls = kwargs.get('urls', None)
        self.files = kwargs.get('files', None)
