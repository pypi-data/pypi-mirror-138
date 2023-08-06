from dataclasses import dataclass
from typing import Any

from pyrinth.model.v2.enums import HashAlgorithm


__all__ = [
	'VersionFile'
]


@dataclass
class VersionFile:
	hashes: dict[ HashAlgorithm, str ]  #:
	url: str  #:
	filename: str  #:
	primary: bool  #:

	@classmethod
	def fromJson( cls, kwargs: dict ) -> 'VersionFile':
		kwargs[ 'hashes' ] = HashAlgorithm.forDict( kwargs['hashes'] )

		return VersionFile( **kwargs )

	@classmethod
	def forList( cls, versionList: list[ dict[ str, Any ] ] ) -> list[ 'VersionFile' ]:
		versions = []
		for version in versionList:
			versions.append( VersionFile( **version ) )

		return versions
