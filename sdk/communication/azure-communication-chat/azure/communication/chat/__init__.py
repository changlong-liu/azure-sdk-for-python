from ._version import VERSION
from ._chat_client import ChatClient
from ._chat_thread_client import ChatThreadClient

__all__ = [
    'ChatClient',
    'ChatThreadClient'
]
__version__ = VERSION
