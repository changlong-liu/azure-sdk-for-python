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

    :ivar identifier: Communication user identifier.
    :vartype identifier: str
    :param identifier: Identifier to initialize CommunicationUser.
    :type identifier: str
    """
    def __init__(self, identifier):
        self.identifier = identifier

class PhoneNumber(CommunicationIdentifier):
    """
    Represents a phone number.

    :ivar value: Value for a phone number.
    :vartype value: str
    :param value: Value to initialize PhoneNumber.
    :type value: str
    """
    def __init__(self, value):
        self.value = value

class UnknownIdentifier(CommunicationIdentifier):
    """
    Represents an identifier of an unknown type.
    It will be encountered in communications with endpoints that are not
    identifiable by this version of the SDK.

    :ivar identifier: Unknown communication identifier.
    :vartype identifier: str
    :param identifier: Value to initialize UnknownIdentifier.
    :type identifier: str
    """
    def __init__(self, identifier):
        self.identifier = identifier
