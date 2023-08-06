from typing import Optional

import requests
from requests import Response


class SessionManager:
	_authToken: Optional[ str ] = None

	def get( self, url: str ) -> Response:
		headers = {
			'Authorization': self._authToken
		}
		params = {}
		return requests.get( headers=headers, url=url, params=params )

	def setGithubToken( self, authToken: Optional[ str ] ):
		self._authToken = authToken

	@classmethod
	def instance( cls ) -> 'SessionManager':
		return _manager


_manager: SessionManager = SessionManager()
