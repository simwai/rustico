import warnings
from typing import Any

from .rustico import (
  Err,
  Ok,
  Result,
  UnwrapError,
  as_async_result,
  as_result,
  catch,
  catch_async,
  do,
  do_async,
  is_err,
  is_ok,
  match,
)

__all__ = [
  'Err',
  'Ok',
  'OkErr',
  'Result',
  'UnwrapError',
  'as_async_result',
  'as_result',
  'catch',
  'catch_async',
  'do',
  'do_async',
  'is_err',
  'is_ok',
  'match',
]


def __getattr__(name: str) -> Any:
  if name == 'OkErr':
    warnings.warn(
      'OkErr is deprecated and will be removed in v2.0. Use (Ok, Err) directly instead.',
      DeprecationWarning,
      stacklevel=2,
    )
    return (Ok, Err)
  msg = f"module 'rustico' has no attribute {name!r}"
  raise AttributeError(msg)
