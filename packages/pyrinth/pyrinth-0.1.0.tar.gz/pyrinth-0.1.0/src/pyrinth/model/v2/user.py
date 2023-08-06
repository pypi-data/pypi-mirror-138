from dataclasses import dataclass
from datetime import datetime

from pyrinth._util import datetimeFromString
from pyrinth.internal.cacheManager import CachedObject
from pyrinth.internal.lazy import LazyObject
from pyrinth.model import v2
from pyrinth.model.v2.enums import UserRole


__all__ = [
	'User',
	'LazyUser'
]


@dataclass
class User:
	username: str  #: The user's username
	name: str  #: The user's display name
	email: str  #: The user's email
	bio: str  #: A description of the user
	id: str  #: The user's id
	github_id: int  #: The user's github id
	avatar_url: str  #: The user's avatar url
	created: datetime  #: The time at which the user was created
	role: UserRole  #: The user's role

	@classmethod
	def fromJson( cls, kwargs: dict ) -> 'User':
		kwargs['created'] = datetimeFromString( kwargs['created'] )
		kwargs['role'] = UserRole[ kwargs['role'].upper() ]

		return User( **kwargs )


class LazyUser( CachedObject[User], LazyObject[User] ):
	def _populate( self ) -> None:
		value = LazyUser.getObject( self._projectid )
		if value is None:
			value = User.fromJson( v2.getRequest( f'user/{self._projectid}' ).json() )
			LazyUser.setObject( self._projectid, self._impl )
		self._impl = value
