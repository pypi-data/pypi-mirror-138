"""
Contains all models and interaction methods for the modrinth v1 API
"""
from warnings import warn

import requests
from requests import Response


from .versionFile import VersionFile
from .version import Version, LazyVersion
from .mod import Mod, LazyMod
from .user import User, LazyUser

warn( 'This is deprecated, use v2', DeprecationWarning, stacklevel=2 )


def getRequest( path: str ) -> Response:
	return requests.get(f'https://api.modrinth.com/api/v1/{path}')
