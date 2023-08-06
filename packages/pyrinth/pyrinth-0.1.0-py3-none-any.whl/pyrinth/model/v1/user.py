from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from warnings import warn

import pyrinth.model.v1 as v1
from pyrinth import _util
from pyrinth.internal.cacheManager import CachedObject
from pyrinth.internal.lazy import LazyObject
from pyrinth.model.v1.enums import UserRole


__all__ = [
	'User',
	'LazyUser'
]


warn( 'This is deprecated, use v2', DeprecationWarning, stacklevel=2 )


@dataclass(frozen=True)
class User:
	""" Represents an user on modrinth"""
	id: str
	github_id: Optional[int]
	username: str
	name: str
	email: Optional[str]
	avatar_url: Optional[str]
	bio: str
	created: datetime
	role: UserRole

	@classmethod
	def fromJson( cls, kwargs ) -> 'User':
		""" Deserializes a Mod object from a dict """
		kwargs['created'] = _util.datetimeFromString( kwargs['created'] )
		kwargs['role'] = UserRole[ kwargs['role'].upper() ]
		return User( **kwargs )


class LazyUser( CachedObject[User], LazyObject[User] ):
	""" An `User` class that only loads its attributes when requested """
	_userid: str

	def __init__( self, userid: str ):
		self._userid = userid

	def _populate( self ) -> None:
		value = LazyUser.getObject( self._userid )
		if value is None:
			self._impl = User.fromJson( v1.getRequest( f'user/{self._userid}' ).json() )
			LazyUser.setObject( self._userid, self._impl )
		else:
			self._impl = value