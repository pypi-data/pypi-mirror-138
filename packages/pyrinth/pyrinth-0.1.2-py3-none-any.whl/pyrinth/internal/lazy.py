from abc import abstractmethod, ABCMeta
from typing import Any, Generic, TypeVar, cast

T = TypeVar('T')


class LazyObject( Generic[T], metaclass=ABCMeta ):
	""" An abstract class for objects that will load their attributes only when requested to """
	_impl: T = None  # type: ignore

	def __getattr__( self, item: str ) -> Any:
		self._checkPopulated()
		return getattr( self._impl, item )

	def __repr__( self ) -> str:
		return self.__getattr__( '__repr__' )()

	def __eq__( self, other: object ) -> bool:
		if not isinstance( other, LazyObject ):
			return False
		other._checkPopulated()
		return self.__getattr__( '__eq__' )( other._impl )

	def _checkPopulated( self ) -> None:
		# if the object was not populated, populate it
		if self._impl is None:
			self._populate()

	@abstractmethod
	def _populate( self ) -> None: ...

	@classmethod
	def forId( cls, objid: str ) -> T:
		""" Returns a lazy wrapper for the object of type T """
		# noinspection PyArgumentList
		return cast( T, cls( objid ) )  # type: ignore
