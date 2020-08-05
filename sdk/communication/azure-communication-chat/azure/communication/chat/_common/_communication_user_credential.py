# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import six

class CommunicationUserCredential(object):
    """Credential type used for authenticating to an Azure Communication service.
    :param str token: The token used to authenticate to an Azure Communication service
    :raises: TypeError
    """


    def __init__(self, token):
        # type: (str) -> None
        if not isinstance(token, six.string_types):
            raise TypeError("token must be a string.")
        self._token = token  # type: str

    @property
    def token(self):
        # type () -> str
        """The value of the configured token.
        :rtype: str
        """
        return self._token