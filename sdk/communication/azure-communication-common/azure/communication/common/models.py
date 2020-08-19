# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

class CommunicationIdentifier:
    """
    Represents an identifier in Azure Communication Service.
    """

class CommunicationUser(CommunicationIdentifier):
    """
    Represents a user in Azure Communication Service.
    """
    def __init__(self, userid):
        self.userid = userid

class PhoneNumber(CommunicationIdentifier):
    """
    Represents a phone number.
    """
    def __init__(self, value):
        self.value = value

class UnknownIdentifier(CommunicationIdentifier):
    """
    Represents an identifier of an unknown type.
    It will be encountered in communications with endpoints that are not
    identifiable by this version of the SDK.
    """
    def __init__(self, identifier):
        self.identifier = identifier
