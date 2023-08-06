from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from warnings import warn

from pyrinth._util import Deprecated
from pyrinth.internal.cacheManager import CachedObject
from pyrinth.internal.lazy import LazyObject
import pyrinth.model.v1 as v1


__all__ = [
	'Version',
	'LazyVersion'
]


warn( 'This is deprecated, use v2', DeprecationWarning, stacklevel=2 )


@dataclass(frozen=True)
class Version:
	""" Represents a mod version on modrinth, it may have more than one file associated with it """
	id: str
	mod_id: str
	author_id: str
	featured: bool
	name: str
	version_number: str
	changelog: Optional[str]
	date_published: datetime
	downloads: int
	version_type: str
	files: list[str]
	dependencies: list[str]
	game_versions: list[str]
	loaders: list[str]
	changelog_url: Optional[str] = Deprecated( reason='Changelog is now directly in the object' )  # type: ignore

	@classmethod
	def fromJson( cls, kwargs ) -> 'Version':
		return Version( **kwargs )


class LazyVersion( CachedObject[Version], LazyObject[Version] ):
	""" A `Version` class that only loads its attributes when requested """
	_verid: str

	def __init__( self, verid: str ):
		self._verid = verid

	def _populate( self ) -> None:
		value = LazyVersion.getObject( self._verid )
		if value is None:
			self._impl = Version.fromJson( v1.getRequest( f'version/{self._verid}' ).json() )
			LazyVersion.setObject( self._verid, self._impl )
		else:
			self._impl = value