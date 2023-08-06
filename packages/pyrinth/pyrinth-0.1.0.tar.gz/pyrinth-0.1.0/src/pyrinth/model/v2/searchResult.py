from dataclasses import dataclass
from typing import Any

from pyrinth.internal.cacheManager import CachedObject
from pyrinth.internal.lazy import LazyObject
from pyrinth.model import v2
from pyrinth.model.license import License
from pyrinth.model.v2.enums import Category, Loader, SortingOrder, ProjectType
from pyrinth.model.v2.project import Project


__all__ = [
	'SearchRequest',
	'SearchResult',
	'LazySearchResult'
]


@dataclass( frozen=True )
class SearchRequest:
	# TODO: Document
	categories: tuple[ Category ]  #: The category to filter the results from
	loaders: tuple[ Loader ]  #: The loader to filter the results from
	limit: int  #: The maximum number of results that will be returned in the response. The maximum limit is 100.
	offset: int  #: The offset field allows for projects to be skipped from the result.
	mcVersions: tuple[ str ]  #: The minecraft versions to filter the results from
	licenses: tuple[ License ]  #: The license ID to filter the results from
	project_types: tuple[ ProjectType ]  #: The project type to filter the results from
	order: SortingOrder = SortingOrder.RELEVANCE  #: Changes the way the results will be sorted in the response.


@dataclass( frozen=True )
class SearchResult:
	# TODO: Document
	search: SearchRequest
	hits: list[ Project ]  #:
	offset: int  #:
	limit: int  #:
	total_hits: int  #:

	@classmethod
	def fromJson( cls, kwargs: dict[ str, Any ], req: SearchRequest ) -> 'SearchResult':
		hits = []
		for hit in kwargs['hits']:
			hits.append( Project.fromJson( hit ) )
		kwargs[ 'hits' ] = hits

		return SearchResult( **kwargs, search=req )


class LazySearchResult( CachedObject[SearchResult], LazyObject[SearchResult] ):
	# TODO: Document
	def _populate( self ) -> None:
		value = LazySearchResult.getObject( str( self.search ) )
		if value is None:
			# TODO: Use correct entrypoint
			value = Project.fromJson( v2.getRequest( f'project/{self._projectid}' ).json() )
			LazySearchResult.setObject( self._projectid, self._impl )
		self._impl = value
