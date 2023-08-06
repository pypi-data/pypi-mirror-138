from dataclasses import dataclass
from warnings import warn

import requests

from pyrinth.model.v1.enums import HashAlgorithm


__all__ = [
	'VersionFile'
]


warn( 'This is deprecated, use v2', DeprecationWarning, stacklevel=2 )


@dataclass
class VersionFile:
	""" A file of a version object """
	hashes: dict[ HashAlgorithm, str ]
	primary: bool
	url: str

	def download( self ) -> bytes:
		""" Downloads this version file and return it as a `bytes` object """
		return requests.get( self.url ).content

	async def adownload( self ) -> bytes:
		return requests.get( self.url ).content
