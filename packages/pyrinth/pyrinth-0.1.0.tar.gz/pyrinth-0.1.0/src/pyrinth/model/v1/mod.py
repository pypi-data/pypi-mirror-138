from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from warnings import warn

from pyrinth._util import Deprecated
import pyrinth.model.v1 as v1
from pyrinth import _util
from pyrinth.internal.cacheManager import CachedObject
from pyrinth.internal.lazy import LazyObject
from pyrinth.model.v1.enums import Category, SupportStatus, ModStatus
from pyrinth.model.license import License


warn( 'This is deprecated, use v2', DeprecationWarning, stacklevel=2 )


@dataclass(frozen=True)
class Mod:
	""" A mod is a modification of the game, this class reppresents it in its modrinth model """
	id: str  #: Mod's id
	slug: str
	team: str
	title: str
	description: str
	body: str
	published: datetime
	updated: datetime
	status: ModStatus
	license: License
	client_side: SupportStatus
	server_side: SupportStatus
	downloads: int
	followers: int
	categories: list[Category]
	versions: list[str]
	icon_url: Optional[str]
	issues_url: Optional[str]
	source_url: Optional[str]
	wiki_url: Optional[str]
	discord_url: Optional[str]
	donation_urls: list[str]
	body_url: Optional[str] = Deprecated( 'Body is now included in the object directly' )  # type: ignore

	@classmethod
	def fromJson( cls, kwargs ) -> 'Mod':
		""" Deserializes a Mod object from a dict """
		kwargs['published'] = _util.datetimeFromString(  kwargs['published'] )
		kwargs['updated'] = _util.datetimeFromString(  kwargs['updated'] )
		kwargs['status'] = ModStatus[ kwargs['status'].upper() ]
		kwargs['client_side'] = SupportStatus[ kwargs['client_side'].upper() ]
		kwargs['server_side'] = SupportStatus[ kwargs['server_side'].upper() ]
		kwargs['license'] = License.of( **kwargs['license'] )
		kwargs['categories'] = Category.fromList( kwargs['categories'] )
		return Mod( **kwargs )


class LazyMod( CachedObject[Mod], LazyObject[Mod] ):
	""" A `Mod` class that only loads its attributes when requested """
	_modid: str

	def __init__( self, modid: str ):
		self._modid = modid

	def _populate( self ) -> None:
		value = LazyMod.getObject( self._modid )
		if value is None:
			self._impl = Mod.fromJson( v1.getRequest( f'mod/{self._modid}' ).json() )
			LazyMod.setObject( self._modid, self._impl )
		else:
			self._impl = value
