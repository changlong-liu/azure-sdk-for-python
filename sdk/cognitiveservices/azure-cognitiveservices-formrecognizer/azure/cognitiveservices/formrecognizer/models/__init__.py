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

try:
    from .train_source_filter_py3 import TrainSourceFilter
    from .train_request_py3 import TrainRequest
    from .form_document_report_py3 import FormDocumentReport
    from .form_operation_error_py3 import FormOperationError
    from .train_result_py3 import TrainResult
    from .keys_result_py3 import KeysResult
    from .model_result_py3 import ModelResult
    from .models_result_py3 import ModelsResult
    from .inner_error_py3 import InnerError
    from .error_information_py3 import ErrorInformation
    from .error_response_py3 import ErrorResponse, ErrorResponseException
    from .extracted_token_py3 import ExtractedToken
    from .extracted_key_value_pair_py3 import ExtractedKeyValuePair
    from .extracted_table_column_py3 import ExtractedTableColumn
    from .extracted_table_py3 import ExtractedTable
    from .extracted_page_py3 import ExtractedPage
    from .analyze_result_py3 import AnalyzeResult
    from .word_py3 import Word
    from .line_py3 import Line
    from .text_recognition_result_py3 import TextRecognitionResult
    from .element_reference_py3 import ElementReference
    from .field_value_py3 import FieldValue
    from .understanding_result_py3 import UnderstandingResult
    from .analyze_receipt_result_py3 import AnalyzeReceiptResult
    from .string_value_py3 import StringValue
    from .number_value_py3 import NumberValue
    from .image_url_py3 import ImageUrl
except (SyntaxError, ImportError):
    from .train_source_filter import TrainSourceFilter
    from .train_request import TrainRequest
    from .form_document_report import FormDocumentReport
    from .form_operation_error import FormOperationError
    from .train_result import TrainResult
    from .keys_result import KeysResult
    from .model_result import ModelResult
    from .models_result import ModelsResult
    from .inner_error import InnerError
    from .error_information import ErrorInformation
    from .error_response import ErrorResponse, ErrorResponseException
    from .extracted_token import ExtractedToken
    from .extracted_key_value_pair import ExtractedKeyValuePair
    from .extracted_table_column import ExtractedTableColumn
    from .extracted_table import ExtractedTable
    from .extracted_page import ExtractedPage
    from .analyze_result import AnalyzeResult
    from .word import Word
    from .line import Line
    from .text_recognition_result import TextRecognitionResult
    from .element_reference import ElementReference
    from .field_value import FieldValue
    from .understanding_result import UnderstandingResult
    from .analyze_receipt_result import AnalyzeReceiptResult
    from .string_value import StringValue
    from .number_value import NumberValue
    from .image_url import ImageUrl
from .form_recognizer_client_enums import (
    OperationStatusCodes,
    TextRecognitionResultDimensionUnit,
    TextRecognitionResultConfidenceClass,
)

__all__ = [
    'TrainSourceFilter',
    'TrainRequest',
    'FormDocumentReport',
    'FormOperationError',
    'TrainResult',
    'KeysResult',
    'ModelResult',
    'ModelsResult',
    'InnerError',
    'ErrorInformation',
    'ErrorResponse', 'ErrorResponseException',
    'ExtractedToken',
    'ExtractedKeyValuePair',
    'ExtractedTableColumn',
    'ExtractedTable',
    'ExtractedPage',
    'AnalyzeResult',
    'Word',
    'Line',
    'TextRecognitionResult',
    'ElementReference',
    'FieldValue',
    'UnderstandingResult',
    'AnalyzeReceiptResult',
    'StringValue',
    'NumberValue',
    'ImageUrl',
    'OperationStatusCodes',
    'TextRecognitionResultDimensionUnit',
    'TextRecognitionResultConfidenceClass',
]
