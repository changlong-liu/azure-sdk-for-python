# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

class QueryStringConstants(object):
    SIGNED_SIGNATURE = 'sig'
    SIGNED_PERMISSION = 'sp'
    SIGNED_START = 'st'
    SIGNED_EXPIRY = 'se'
    SIGNED_RESOURCE = 'sr'
    SIGNED_IDENTIFIER = 'si'
    SIGNED_IP = 'sip'
    SIGNED_PROTOCOL = 'spr'
    SIGNED_VERSION = 'sv'
    SIGNED_CACHE_CONTROL = 'rscc'
    SIGNED_CONTENT_DISPOSITION = 'rscd'
    SIGNED_CONTENT_ENCODING = 'rsce'
    SIGNED_CONTENT_LANGUAGE = 'rscl'
    SIGNED_CONTENT_TYPE = 'rsct'
    START_PK = 'spk'
    START_RK = 'srk'
    END_PK = 'epk'
    END_RK = 'erk'
    SIGNED_RESOURCE_TYPES = 'srt'
    SIGNED_SERVICES = 'ss'
    SIGNED_OID = 'skoid'
    SIGNED_TID = 'sktid'
    SIGNED_KEY_START = 'skt'
    SIGNED_KEY_EXPIRY = 'ske'
    SIGNED_KEY_SERVICE = 'sks'
    SIGNED_KEY_VERSION = 'skv'

    @staticmethod
    def to_list():
        return [
            QueryStringConstants.SIGNED_SIGNATURE,
            QueryStringConstants.SIGNED_PERMISSION,
            QueryStringConstants.SIGNED_START,
            QueryStringConstants.SIGNED_EXPIRY,
            QueryStringConstants.SIGNED_RESOURCE,
            QueryStringConstants.SIGNED_IDENTIFIER,
            QueryStringConstants.SIGNED_IP,
            QueryStringConstants.SIGNED_PROTOCOL,
            QueryStringConstants.SIGNED_VERSION,
            QueryStringConstants.SIGNED_CACHE_CONTROL,
            QueryStringConstants.SIGNED_CONTENT_DISPOSITION,
            QueryStringConstants.SIGNED_CONTENT_ENCODING,
            QueryStringConstants.SIGNED_CONTENT_LANGUAGE,
            QueryStringConstants.SIGNED_CONTENT_TYPE,
            QueryStringConstants.START_PK,
            QueryStringConstants.START_RK,
            QueryStringConstants.END_PK,
            QueryStringConstants.END_RK,
            QueryStringConstants.SIGNED_RESOURCE_TYPES,
            QueryStringConstants.SIGNED_SERVICES,
            QueryStringConstants.SIGNED_OID,
            QueryStringConstants.SIGNED_TID,
            QueryStringConstants.SIGNED_KEY_START,
            QueryStringConstants.SIGNED_KEY_EXPIRY,
            QueryStringConstants.SIGNED_KEY_SERVICE,
            QueryStringConstants.SIGNED_KEY_VERSION,
        ]