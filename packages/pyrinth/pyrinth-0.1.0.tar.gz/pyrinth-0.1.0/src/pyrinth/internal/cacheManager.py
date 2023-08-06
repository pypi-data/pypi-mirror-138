from abc import ABCMeta
from dataclasses import dataclass
from typing import Generic, TypeVar, Type, Optional
from time import time

T = TypeVar('T')


@dataclass(frozen=True)
class TimedObject( Generic[T] ):
	""" Utility wrapper for `CachedObject`s with a creation timestamp  """
	creationTime: float
	object: T


class CacheManager:
	""" Manages `CachedObject`s lifetime and persistence"""
	_maxCacheLifeSeconds: int = 480
	_cache: dict[ Type[T], dict[ str, TimedObject[T] ] ]  # type: ignore

	def __init__(self):
		self._cache = dict()

	def __getitem__(self, item: tuple[ Type[T], str ] ) -> Optional[T]:
		"""
		Method responsible for:
		 - Checking whether a cache entry is outdated
		 - Checking if a cache entry exists
		:param item: A class-id tuple
		:returns: None if the entry doesn't exist or is outdated, else the entry's object
		"""
		if item[0] in self._cache:
			obj = self._cache[ item[0] ].get( item[1] )
			if obj is not None and time() - obj.creationTime < self._maxCacheLifeSeconds:
				return obj.object
		return None

	def __setitem__(self, key: tuple[ Type[T], str ], value: T ) -> None:
		"""
		Method responsible for:
		 - Creating a cache entry for an object
		 - Creating a cache class for an object's class
		:param key: A class-id tuple
		:param value: The object to set the cache entry to
		"""
		if key[0] not in self._cache:
			self._cache[ key[0] ] = {}
		self._cache[ key[0] ][ key[1] ] = TimedObject( time(), value )


class CachedObject( Generic[T], metaclass=ABCMeta ):
	""" An object that can be cached and timestamped """

	@classmethod
	def setObject( cls, objid: str, obj: T ) -> None:
		manager[ cls, objid ] = obj

	@classmethod
	def getObject( cls, objid: str ) -> Optional[T]:
		return manager[ cls, objid ]  # type: ignore


manager = CacheManager()  #: `CacheManager` singleton
