import warnings
from datetime import datetime
from typing import Generic, TypeVar


T = TypeVar('T')


def datetimeFromString( string: str ) -> datetime:
	# 2021-02-24T22:24:59.182336Z
	date, time = string.split('T')
	return datetime(
		*[ int( part ) for part in date.split('-') ],  # type: ignore
		*[ int( float( part ) ) for part in time[:-1].split(':') ]
	)


class Deprecated(Generic[T]):
	""" Decorator for deprecated fields, classes, methods and functions """
	_NO_FIELD_VALUE = object()
	_reason: str = ''
	_field: T | object = _NO_FIELD_VALUE

	def __init__( self, *args, reason: str = None ) -> None:
		if reason is not None:
			self._reason = reason
		else:
			self._field = args[0]

	def __get__( self, instance, owner ) -> T:
		warnings.warn(
			message=self._reason,
			category=DeprecationWarning,
			stacklevel=2
		)
		return self._field  # type: ignore

	def __set__( self, instance, value: T ) -> None:
		if self._field is not Deprecated._NO_FIELD_VALUE:
			warnings.warn(
				message=self._reason,
				category=DeprecationWarning,
				stacklevel=2
			)
		self._field = value

	def __repr__(self) -> str:
		return self._field.__repr__()

	def __call__(self, *args, **kwargs):
		if self._field is Deprecated._NO_FIELD_VALUE:
			self._field = args[0]
			return self
		warnings.warn(
			message=self._reason,
			category=DeprecationWarning,
			stacklevel=2
		)
		return self._field( *args, **kwargs )
