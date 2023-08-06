"""
Contains all models and interaction methods for the modrinth v2 API
"""
from requests import Response

from pyrinth.internal.sessionManager import SessionManager
from pyrinth.model.v2.searchResult import SearchResult

__all__ = [
	'getRequest'
]


def getRequest( path: str ) -> Response:
	return SessionManager.instance().get(f'https://api.modrinth.com/v2/{path}')

