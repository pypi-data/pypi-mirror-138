from enum import Enum
from warnings import warn


__all__ = [
	'Category',
	'SupportStatus',
	'ModStatus',
	'UserRole',
	'HashAlgorithm'
]


warn( 'This is deprecated, use v2', DeprecationWarning, stacklevel=2 )


class Category(Enum):
	""" Categories a mod may be in """
	TECNOLOGY = 'tecnology'
	ADVENTURE = 'adventure'
	MAGIC = 'magic'
	UTILITY = 'utility'
	DECORATION = 'decoration'
	LIBRARY = 'library'
	CURSED = 'cursed'
	WORLDGEN = 'worldgen'
	STORAGE = 'storage'
	FOOD = 'food'
	EQUIPMENT = 'equipment'
	MISC = 'misc'

	@classmethod
	def fromList( cls, categories: list[str] ) -> list['Category']:
		cats = []
		for category in categories:
			cats.append( cls[ category.upper() ] )

		return cats


class SupportStatus(Enum):
	""" Whether this mod supports being in a certain enviroment """
	REQUIRED = 'required'
	OPTIONAL = 'optional'
	UNSUPPORTED = 'unsupported'
	UNKNOWN = 'unknown'  #: No longer exists in v2


class UserRole(Enum):
	""" A user's role in the modrinth platform """
	DEVELOPER = 'developer'
	MODERATOR = 'moderator'
	ADMIN = 'admin'


class ModStatus(Enum):
	""" Whether a mod has been approved or not """
	APPROVED = 'approved'
	REJECTED = 'rejected'


class HashAlgorithm(Enum):
	""" Possible hash algorithms used by modrinth """
	SHA512 = 'sha512'
	SHA1 = 'sha1'
	UNKNOWN = 'unknown'

	@classmethod
	def forString( cls, string: str ) -> 'HashAlgorithm':
		try:
			return HashAlgorithm[ string ]
		except KeyError:
			return HashAlgorithm.UNKNOWN
