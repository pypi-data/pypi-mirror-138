from dataclasses import dataclass

__all__ = [
	'License',
	'Licenses'
]


@dataclass( frozen=True )
class License:
	""" Represents a license """
	id: str  #: License id
	name: str  #: License full name
	url: str | None  #: License url, usually from the modrinth CDN ( None when ARR )

	@classmethod
	def of( cls, id: str, name: str, url: str ) -> 'License':
		""" Returns the correct license object based on the ID and URL """
		match id:
			case 'lgpl':
					return Licenses.LGPL
			case 'apache':
				return Licenses.APACHE
			case 'bsd-2-clause':
				return Licenses.BSD_2_CLAUSE
			case 'bsd-3-clause':
				return Licenses.BSD_3_CLAUSE
			case 'bsl':
				return Licenses.BSL
			case 'cc0':
				return Licenses.CC0
			case 'unlicense':
				return Licenses.UNLICENSE
			case 'mpl':
				return Licenses.MPL
			case 'mit':
				return Licenses.MIT
			case 'arr':
				return Licenses.ARR
			case 'lgpl-3':
				return Licenses.LGPL3
			case 'custom':
				return Licenses.custom( url )
			case _:
				raise ValueError( f'Unknown license id "{id}"' )


class Licenses:
	""" Object that holds all licenses """
	CUSTOMS: list[ License ] = []  #: List that holds all custom license objects
	LGPL: License = License( 'lgpl', 'GNU Lesser General Public License v2.1', 'https://cdn.modrinth.com/licenses/lgpl.txt' )
	APACHE: License = License( 'apache', 'Apache License 2.0', 'https://cdn.modrinth.com/licenses/apache.txt' )
	BSD_2_CLAUSE: License = License( 'bsd-2-clause', 'BSD 2-Clause', 'https://cdn.modrinth.com/licenses/bsd-2-clause.txt' )
	BSD_3_CLAUSE: License = License( 'bsd-3-clause', 'BSD 3-Clause', 'https://cdn.modrinth.com/licenses/bsd-3-clause.txt' )
	BSL: License = License( 'bsl', 'Boost Software License 1.0', 'https://cdn.modrinth.com/licenses/bsl.txt' )
	CC0: License = License( 'cc0', 'Creative Commons Zero v1.0 Universal', 'https://cdn.modrinth.com/licenses/cc0.txt' )
	UNLICENSE: License = License( 'unlicense', 'The Unlicense', 'https://cdn.modrinth.com/licenses/unlicense.txt' )
	MPL: License = License( 'mpl', 'Mozilla Public License 2.0', 'https://cdn.modrinth.com/licenses/mpl.txt' )
	MIT: License = License( 'mit', 'MIT License', 'https://cdn.modrinth.com/licenses/mit.txt' )
	ARR: License = License( 'arr', 'All Rights Reserved', None )
	LGPL3: License = License( 'lgpl-3', 'GNU Lesser General Public License v3', 'https://cdn.modrinth.com/licenses/lgpl-3.txt' )

	@staticmethod
	def custom( url: str ) -> License:
		""" Returns the correct custom License object for a given url ( may create a new one ) """
		# noinspection PyShadowingBuiltins
		for license in Licenses.CUSTOMS:
			if url == license.url:
				return license
		Licenses.CUSTOMS.append( License( 'custom', 'Custom License', url ) )
		return Licenses.CUSTOMS[ -1 ]
