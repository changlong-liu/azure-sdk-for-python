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


class TextRecognitionResult(Model):
    """Text recognition result from a page in the input document.

    All required parameters must be populated in order to send to Azure.

    :param page: The 1-based page number of the recognition result.
    :type page: int
    :param clockwise_orientation: The orientation of the image in clockwise
     direction, measured in degrees between [0, 360).
    :type clockwise_orientation: float
    :param width: The width of the image/PDF in pixels/inches, respectively.
    :type width: float
    :param height: The height of the image/PDF in pixels/inches, respectively.
    :type height: float
    :param unit: The unit used by the width, height and boundingBox
     properties. For images, the unit is "pixel". For PDF, the unit is "inch".
     Possible values include: 'pixel', 'inch'
    :type unit: str or
     ~azure.cognitiveservices.formrecognizer.models.TextRecognitionResultDimensionUnit
    :param lines: Required. A list of recognized text lines. The maximum
     number of lines returned is 300 per page.
     The lines are sorted top to bottom, left to right, although in certain
     cases proximity is treated with higher priority. As the sorting order
     depends on the detected text, it may change across images and OCR version
     updates. Thus, business logic should be built upon the actual line
     location instead of order.
    :type lines: list[~azure.cognitiveservices.formrecognizer.models.Line]
    """

    _validation = {
        'lines': {'required': True},
    }

    _attribute_map = {
        'page': {'key': 'page', 'type': 'int'},
        'clockwise_orientation': {'key': 'clockwiseOrientation', 'type': 'float'},
        'width': {'key': 'width', 'type': 'float'},
        'height': {'key': 'height', 'type': 'float'},
        'unit': {'key': 'unit', 'type': 'TextRecognitionResultDimensionUnit'},
        'lines': {'key': 'lines', 'type': '[Line]'},
    }

    def __init__(self, *, lines, page: int=None, clockwise_orientation: float=None, width: float=None, height: float=None, unit=None, **kwargs) -> None:
        super(TextRecognitionResult, self).__init__(**kwargs)
        self.page = page
        self.clockwise_orientation = clockwise_orientation
        self.width = width
        self.height = height
        self.unit = unit
        self.lines = lines
