"""
PyRinth
-
A library to interact with modrinth's v1 and v2 APIs

Features:

 - Compatible with both v1 and v2 APIs
 - Automatic request caching and refreshing with configurable interval
 - Lazy population of objects to minimize API calls
"""
from pyrinth.internal.sessionManager import SessionManager


__all__ = [
	'init'
]
__version__ = '0.1.1'

__pdoc__ = { 'pyrinth.internal': False }


def init( authToken: str = None ) -> None:
	"""
	:param authToken: GitHub auth token for modrinth auth
	"""
	SessionManager.instance().setGithubToken( authToken )
