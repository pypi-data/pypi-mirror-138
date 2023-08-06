from enum import Enum


__all__ = [
	'Category',
	'SupportStatus',
	'UserRole',
	'ProjectStatus',
	'HashAlgorithm',
	'ProjectType',
	'VersionType',
	'Loader'
]


class Category(Enum):
	""" Categories a project may be in """
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
	def forList( cls, categories: list[str ] ) -> list[ 'Category' ]:
		cats = []
		for category in categories:
			cats.append( cls[ category.upper() ] )

		return cats


class SupportStatus(Enum):
	""" Whether this project supports being in a certain enviroment """
	REQUIRED = 'required'
	OPTIONAL = 'optional'
	UNSUPPORTED = 'unsupported'


class UserRole(Enum):
	""" A user's role in the modrinth platform """
	DEVELOPER = 'developer'
	MODERATOR = 'moderator'
	ADMIN = 'admin'


class ProjectStatus( Enum ):
	""" A project's status on the platform, affects a project's visibility """
	APPROVED = 'approved'
	REJECTED = 'rejected'
	DRAFT = 'draft'
	UNLISTED = 'unlisted'
	PROCESSING = 'processing'
	UNKNOWN = 'unknown'


class HashAlgorithm(Enum):
	""" Possible hash algorithms used by modrinth """
	SHA512 = 'sha512'
	SHA1 = 'sha1'
	UNKNOWN = 'unknown'  #: Custom value

	@classmethod
	def forString( cls, string: str ) -> 'HashAlgorithm':
		try:
			return HashAlgorithm[ string ]
		except KeyError:
			return HashAlgorithm.UNKNOWN

	@classmethod
	def forDict( cls, hashes: dict[ str, str ] ) -> dict[ 'HashAlgorithm', str ]:
		phashes = {}
		for algorithm, value in hashes.items():
			phashes[ HashAlgorithm.forString( algorithm ) ] = value
		return phashes


class ProjectType(Enum):
	""" A project may be a modpack or a mod/plugin """
	MOD = 'mod'
	MODPACK = 'modpack'


class VersionType(Enum):
	""" Release type of version """
	RELEASE = 'release'
	BETA = 'beta'
	ALPHA = 'alpha'


class Loader(Enum):
	""" The mod/plugin loader that this project supports """
	FABRIC = 'fabric'
	FORGE = 'forge'
	BUKKIT = 'bukkit'  #: Not yet part of the v2
	PAPER = 'paper'  #: Not yet part of the v2
	PURPUR = 'purpur'  #: Not yet part of the v2
	SPIGOT = 'spigot'  #: Not yet part of the v2
	SPONGE = 'sponge'  #: Not yet part of the v2

	@classmethod
	def forList( cls, loaders: list[str ] ) -> list[ 'Loader' ]:
		final = []
		for loader in loaders:
			final.append( Loader[ loader.upper() ] )
		return final


class SortingOrder(Enum):
	""" Changes the way the results will be sorted in the search response """
	RELEVANCE = 'relevance'  #: This sorts by the element that our system is the best match for your query.
	DOWNLOADS = 'downloads'  #: This sorts all matches by the order of downloads.
	FOLLOWS = 'follows'  #: The same principle as downloads, but sorted by the number of followers of this mod.
	NEWEST = 'newest'  #: Sorts by the newest mod created. This is based on the time of initial creation of the mod.
	UPDATED = 'updated'  #: Sorts by the newest mod updated. This is based on the time of the latest update of the mod.

