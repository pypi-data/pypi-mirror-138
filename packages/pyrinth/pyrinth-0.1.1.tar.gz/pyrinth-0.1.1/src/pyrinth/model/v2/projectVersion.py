from dataclasses import dataclass
from datetime import datetime
from typing import Any

from pyrinth._util import Deprecated, datetimeFromString
from pyrinth.internal.cacheManager import CachedObject
from pyrinth.internal.lazy import LazyObject
from pyrinth.model.v2.enums import VersionType, Loader
from pyrinth.model.v2.versionFile import VersionFile
import pyrinth.model.v2 as v2


__all__ = [
	'ProjectVersion',
	'LazyProjectVersion'
]


@dataclass
class ProjectVersion:
	name: str  #: The name of this version
	version_number: str  #: The version number. Ideally will follow semantic versioning
	changelog: str  #: The changelog for this version
	dependencies: list[str]  #: A list of specific versions of projects that this version depends on
	game_versions: list[str]  #: A list of versions of Minecraft that this version supports
	version_type: VersionType  #: The release channel for this version
	loaders: list[ Loader ]  #: The mod loaders that this version supports
	featured: bool  #: Whether the version is featured or not
	id: str  #: The ID of the version, encoded as a base62 string
	project_id: str  #: The ID of the project this version is for
	author_id: str  #: The ID of the author who published this version
	date_published: datetime  #:
	downloads: int  #: The number of times this version has been downloaded
	files: list[ VersionFile ]  #: A list of files available for download for this version
	changelog_url: Deprecated[str] = Deprecated( 'Body is now included in the object directly' )  #: A link to the changelog for this version

	@classmethod
	def fromJson( cls, kwargs: dict[ str, Any ] ) -> 'ProjectVersion':
		kwargs['version_type'] = VersionType[ kwargs['version_type'].upper() ]
		kwargs['loaders'] = Loader.forList( kwargs[ 'loaders' ] )
		kwargs['date_published'] = datetimeFromString( kwargs['date_published'] )
		kwargs['files'] = VersionFile.forList( kwargs[ 'files' ] )

		return cls( **kwargs )

	@classmethod
	def forList( cls, versionList: list[ str ] ) -> list[ 'ProjectVersion' ]:
		versions = []
		for version in versionList:
			versions.append( LazyProjectVersion.forId(version) )
		
		return versions


class LazyProjectVersion( CachedObject[ ProjectVersion ], LazyObject[ ProjectVersion ] ):
	_projectversionid: str

	def __init__( self, projectversionid: str ):
		self._projectversionid = projectversionid

	def _populate( self ) -> None:
		value = LazyProjectVersion.getObject( self._projectversionid )
		if value is None:
			value = ProjectVersion.fromJson( v2.getRequest( f'version/{self._projectversionid}' ).json() )
			LazyProjectVersion.setObject( self._projectversionid, self._impl )
		self._impl = value
