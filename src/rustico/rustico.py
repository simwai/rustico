from __future__ import annotations

import functools
import inspect
import traceback
import warnings
from collections.abc import AsyncGenerator, Awaitable, Callable, Generator
from typing import Any, Generic, Literal, NoReturn, TypeVar, cast

try:
  from typing import ParamSpec
except ImportError:
  try:
    from typing_extensions import ParamSpec
  except ImportError:
    raise ImportError('rustico requires `typing_extensions` on Python <3.10 for ParamSpec support') from None

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from typing_extensions import TypeIs

T = TypeVar('T')
U = TypeVar('U')
F = TypeVar('F')
E = TypeVar('E')
R = TypeVar('R')
P = ParamSpec('P')  # Captures the parameter types of the decorated function.
BE = TypeVar('BE', bound=BaseException)


class Result(Generic[T, E]):
  """Base class for Ok (success) and Err (failure) variants.

  Use this for isinstance checks instead of the deprecated OkErr tuple.
  Use Ok/Err methods directly for type-specific functionality.

  ```
  isinstance(Ok(42), Result)  # True
  isinstance(Err("fail"), Result)  # True
  ```
  """

  __slots__ = ()

  def is_ok(self) -> bool:
    raise NotImplementedError

  def is_err(self) -> bool:
    raise NotImplementedError

  def ok(self) -> T | None:
    raise NotImplementedError

  def err(self) -> E | None:
    raise NotImplementedError

  def unwrap(self) -> T:
    raise NotImplementedError

  def unwrap_err(self) -> E:
    raise NotImplementedError

  def expect(self, message: str) -> T:
    raise NotImplementedError

  def expect_err(self, message: str) -> E:
    raise NotImplementedError

  def value_or(self, default: T) -> T:
    raise NotImplementedError

  def unwrap_or(self, default: T) -> T:
    raise NotImplementedError

  def unwrap_or_else(self, op: Callable[[E], T]) -> T:
    raise NotImplementedError

  def map(self, op: Callable[[T], U]) -> Result[U, E]:
    raise NotImplementedError

  def map_err(self, op: Callable[[E], F]) -> Result[T, F]:
    raise NotImplementedError

  def and_then(self, op: Callable[[T], Result[U, E]]) -> Result[U, E]:
    raise NotImplementedError

  def or_else(self, op: Callable[[E], Result[T, F]]) -> Result[T, F]:
    raise NotImplementedError

  def inspect(self, op: Callable[[T], Any]) -> Result[T, E]:
    raise NotImplementedError

  def inspect_err(self, op: Callable[[E], Any]) -> Result[T, E]:
    raise NotImplementedError

  def match(self, *, ok: Callable[[T], U] | None = None, err: Callable[[E], U] | None = None) -> U:
    raise NotImplementedError

  def alt(self, op: Callable[[E], F]) -> Result[T, F]:
    raise NotImplementedError

  def map_or(self, default: U, op: Callable[[T], U]) -> U:
    raise NotImplementedError

  def map_or_else(self, default_op: Callable[[], U], op: Callable[[T], U]) -> U:
    raise NotImplementedError

  def unwrap_or_raise(self, exception_type: type[BaseException]) -> T:
    raise NotImplementedError

  async def map_async(self, op: Callable[[T], Awaitable[U]]) -> Result[U, E]:
    raise NotImplementedError

  async def and_then_async(self, op: Callable[[T], Awaitable[Result[U, E]]]) -> Result[U, E]:
    raise NotImplementedError


class UnwrapError(Exception, Generic[T, E]):
  """
  Exception raised when an unwrap or expect operation fails on a Result.

  ```
  try:
      Err("fail").unwrap()
  except UnwrapError as e:
      print(e)
  # Called `Result.unwrap()` on an `Err` value: 'fail'
  ```
  """

  _result: Result[T, E]

  def __init__(self, result: Result[T, E], message: str) -> None:
    self._result = result
    super().__init__(message)

  @property
  def result(self) -> Result[T, E]:
    """
    Returns the original result that caused the unwrap failure.

    Useful for debugging and error recovery scenarios where you need to inspect
    the original Result that failed to unwrap. Common in error handling pipelines
    where you want to log the original error context.

    ```
    try:
        Err("fail").unwrap()
    except UnwrapError as e:
        assert isinstance(e.result, Err)
    ```
    """
    return self._result


def _unwrap_error(result: Result[T, E], message: str) -> UnwrapError[T, E]:
  return UnwrapError(result, message)


class Ok(Result[T, E]):
  """
  Represents a successful result containing a value.

  Use when operations succeed and you want to chain further operations.
  Avoid when you need to represent failure states - use Err instead.

  ```
  Ok(42).unwrap()  # 42
  ```
  """

  __match_args__ = ('ok_value',)
  __slots__ = ('_value',)

  def __init__(self, value: T) -> None:
    self._value = value

  def __repr__(self) -> str:
    return f'Ok({self._value!r})'

  def __eq__(self, other: Any) -> bool:
    if not isinstance(other, Ok):
      return False
    other_ok = cast('Ok[T, E]', other)
    return self._value == other_ok._value

  def __ne__(self, other: Any) -> bool:
    return not (self == other)

  def __hash__(self) -> int:
    return hash((True, self._value))

  def is_ok(self) -> Literal[True]:
    return True

  def is_err(self) -> Literal[False]:
    return False

  def ok(self) -> T:
    return self._value

  def err(self) -> None:
    return None

  @property
  def ok_value(self) -> T:
    return self._value

  def value_or(self, default: T) -> T:
    return self.unwrap_or(default)

  def alt(self, op: Callable[[E], F]) -> Ok[T, E]:
    return self.map_err(op)

  def expect(self, message: str) -> T:
    return self._value

  def expect_err(self, message: str) -> NoReturn:
    raise _unwrap_error(self, message)

  def unwrap(self) -> T:
    return self._value

  def unwrap_err(self) -> NoReturn:
    raise _unwrap_error(self, 'Called `Result.unwrap_err()` on an `Ok` value')

  def unwrap_or(self, default: T) -> T:
    return self._value

  def unwrap_or_else(self, op: Callable[[E], T]) -> T:
    return self._value

  def unwrap_or_raise(self, exception_type: type[BaseException]) -> T:
    return self._value

  def map(self, op: Callable[[T], U]) -> Ok[U, E]:
    return Ok(op(self._value))

  async def map_async(self, op: Callable[[T], Awaitable[U]]) -> Ok[U, E]:
    return Ok(await op(self._value))

  def map_or(self, default: U, op: Callable[[T], U]) -> U:
    return op(self._value)

  def map_or_else(self, default_op: Callable[[], U], op: Callable[[T], U]) -> U:
    return op(self._value)

  def map_err(self, op: Callable[[E], F]) -> Ok[T, E]:
    return self

  def and_then(self, op: Callable[[T], Result[U, E]]) -> Result[U, E]:
    return op(self._value)

  async def and_then_async(self, op: Callable[[T], Awaitable[Result[U, E]]]) -> Result[U, E]:
    return await op(self._value)

  def or_else(self, op: Callable[[E], Result[T, F]]) -> Ok[T, E]:
    return self

  def inspect(self, op: Callable[[T], Any]) -> Ok[T, E]:
    op(self._value)
    return self

  def inspect_err(self, op: Callable[[E], Any]) -> Ok[T, E]:
    return self

  def match(self, *, ok: Callable[[T], U] | None = None, err: Callable[[E], U] | None = None) -> U:
    if ok is None:
      raise ValueError("Ok.match requires an 'ok' handler")
    return ok(self._value)


class Err(Result[T, E]):
  """
  Represents a failed result containing an error value.

  Use when operations fail and you want to propagate error information.
  Avoid when success is the only meaningful outcome.

  ```
  Err("fail").unwrap_or(0)  # 0
  ```
  """

  __match_args__ = ('err_value',)
  __slots__ = ('_trace', '_trace_pending', '_value')

  def __init__(self, value: E) -> None:
    self._value = value
    self._trace: list[str] | None = None
    self._trace_pending = isinstance(value, BaseException)

  def _capture_traceback(self, exc: E) -> list[str] | None:
    if isinstance(exc, BaseException) and exc.__traceback__ is not None:
      stack_summary = traceback.extract_tb(exc.__traceback__)
      return traceback.format_list(stack_summary)
    return None

  @property
  def trace(self) -> list[str] | None:
    if self._trace_pending:
      self._trace = self._capture_traceback(self._value)
      self._trace_pending = False
    return self._trace

  def __repr__(self) -> str:
    return f'Err({self._value!r})'

  def __eq__(self, other: Any) -> bool:
    if not isinstance(other, Err):
      return False
    other_err = cast('Err[T, E]', other)
    return self._value == other_err._value

  def __ne__(self, other: Any) -> bool:
    return not (self == other)

  def __hash__(self) -> int:
    return hash((False, self._value))

  def is_ok(self) -> Literal[False]:
    return False

  def is_err(self) -> Literal[True]:
    return True

  def ok(self) -> None:
    return None

  def err(self) -> E:
    return self._value

  @property
  def err_value(self) -> E:
    return self._value

  def value_or(self, default: T) -> T:
    return self.unwrap_or(default)

  def alt(self, op: Callable[[E], F]) -> Result[T, F]:
    return self.map_err(op)

  def expect(self, message: str) -> NoReturn:
    exc = _unwrap_error(self, f'{message}: {self._value!r}')
    if isinstance(self._value, BaseException):
      raise exc from self._value
    raise exc

  def expect_err(self, message: str) -> E:
    return self._value

  def unwrap(self) -> NoReturn:
    exc = _unwrap_error(self, f'Called `Result.unwrap()` on an `Err` value: {self._value!r}')
    if isinstance(self._value, BaseException):
      raise exc from self._value
    raise exc

  def unwrap_err(self) -> E:
    return self._value

  def unwrap_or(self, default: T) -> T:
    return default

  def unwrap_or_else(self, op: Callable[[E], T]) -> T:
    return op(self._value)

  def unwrap_or_raise(self, exception_type: type[BaseException]) -> NoReturn:
    raise exception_type(self._value)

  def map(self, op: Callable[[T], U]) -> Err[T, E]:
    return self

  async def map_async(self, op: Callable[[T], Awaitable[U]]) -> Err[T, E]:
    return self

  def map_or(self, default: U, op: Callable[[T], U]) -> U:
    return default

  def map_or_else(self, default_op: Callable[[], U], op: Callable[[T], U]) -> U:
    return default_op()

  def map_err(self, op: Callable[[E], F]) -> Err[T, F]:
    return Err(op(self._value))

  def and_then(self, op: Callable[[T], Result[U, E]]) -> Err[T, E]:
    return self

  async def and_then_async(self, op: Callable[[T], Awaitable[Result[U, E]]]) -> Err[T, E]:
    return self

  def or_else(self, op: Callable[[E], Result[T, F]]) -> Result[T, F]:
    return op(self._value)

  def inspect(self, op: Callable[[T], Any]) -> Err[T, E]:
    return self

  def inspect_err(self, op: Callable[[E], Any]) -> Err[T, E]:
    op(self._value)
    return self

  def match(self, *, ok: Callable[[T], U] | None = None, err: Callable[[E], U] | None = None) -> U:
    if err is None:
      raise ValueError("Err.match requires an 'err' handler")
    return err(self._value)


def _validate_exception_types(exceptions: tuple[type[BE], ...], decorator_name: str) -> None:
  if not exceptions or not all(isinstance(exc, type) and issubclass(exc, BaseException) for exc in exceptions):  # type: ignore[reportUnnecessaryIsInstance]
    msg = f'{decorator_name}() requires at least one exception type'
    raise TypeError(msg)


def as_result(
  *exceptions: type[BE],
) -> Callable[[Callable[P, T]], Callable[P, Result[T, BE]]]:
  """
  Decorator that converts a function to return Result, catching specified exceptions as Err.

  Use when you want to convert exception-based APIs to Result-based APIs.
  Essential for integrating with existing codebases. Avoid when functions already return Results.

  ```
  @as_result(ValueError)
  def parse_int(x: str) -> int:
      return int(x)

  parse_int("42")  # Ok(42)
  parse_int("fail")  # Err(ValueError(...))
  ```
  """
  _validate_exception_types(exceptions, 'as_result')

  def decorator(f: Callable[P, T]) -> Callable[P, Result[T, BE]]:
    @functools.wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, BE]:
      try:
        return Ok(f(*args, **kwargs))
      except exceptions as exc:
        return Err(exc)

    return wrapper

  return decorator


def as_async_result(
  *exceptions: type[BE],
) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[Result[T, BE]]]]:
  """
  Decorator that converts an async function to return Result, catching specified exceptions as Err.

  Use when you want to convert async exception-based APIs to Result-based APIs.
  Essential for integrating async codebases. Avoid when async functions already return Results.

  ```
  @as_async_result(ValueError)
  async def parse_int_async(x: str) -> int:
      return int(x)
  ```
  """
  _validate_exception_types(exceptions, 'as_async_result')

  def decorator(
    f: Callable[P, Awaitable[T]],
  ) -> Callable[P, Awaitable[Result[T, BE]]]:
    @functools.wraps(f)
    async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, BE]:
      try:
        return Ok(await f(*args, **kwargs))
      except exceptions as exc:
        return Err(exc)

    return async_wrapper

  return decorator


def is_ok(result: Result[T, E]) -> TypeIs[Ok[T, E]]:
  """
  Type guard that returns True if the result is Ok, providing type narrowing.

  Use for type-safe conditional logic and when you need type narrowing.
  Essential for type checkers. Prefer result.is_ok() for simple boolean checks.

  ```
  is_ok(Ok(1))  # True
  is_ok(Err("fail"))  # False
  ```
  """
  return result.is_ok()


def is_err(result: Result[T, E]) -> TypeIs[Err[T, E]]:
  """
  Type guard that returns True if the result is Err, providing type narrowing.

  Use for type-safe conditional logic and when you need type narrowing.
  Essential for type checkers. Prefer result.is_err() for simple boolean checks.

  ```
  is_err(Ok(1))  # False
  is_err(Err("fail"))  # True
  ```
  """
  return result.is_err()


def match(result: Result[T, E], ok_handler: Callable[[T], R], err_handler: Callable[[E], R] | None = None) -> R | None:
  """
  **Deprecated:** Use `result.match(ok=..., err=...)` instead.

  This function is deprecated but remains available for backward compatibility.

    Pattern match on a Result and apply the appropriate handler function.

    This function provides a functional, explicit alternative to Python's pattern matching syntax,
    allowing you to handle both success (`Ok`) and error (`Err`) cases with dedicated handler functions.
    It's especially useful when you want to transform or branch on the contents of a Result
    without unwrapping it or writing conditional logic.

    **When to use:**
    - When you want to handle both success and error cases in a single, readable expression.
    - When you want to transform a Result into another value or type, e.g., for logging, formatting, or fallback logic.
    - When you want to avoid `try/except` and keep error handling explicit and composable.

    **When not to use:**
    - When you only care about the success value and want to fail fast (use `unwrap` or `unwrap_or`).
    - When you only want to transform the success or error value (use `map` or `map_err`).
    - When you need to propagate the Result further without handling it yet.


    ```
    result = get_user_age()  # Returns Result[int, str]
    formatted = match(
        result,
        ok_handler=lambda age: f"User is {age} years old",
        err_handler=lambda err: f"Error getting age: {err}"
    )
    # Ok case: "User is 25 years old"
    # Err case: "Error getting age: Invalid user data"
    ```
  """
  warnings.warn(
    'match() is deprecated, use result.match(ok=..., err=...) instead',
    DeprecationWarning,
    stacklevel=2,
  )
  if result.is_ok():
    return ok_handler(result.unwrap())
  if err_handler is not None:
    return err_handler(result.unwrap_err())
  return None


def do(
  fn_or_gen: Callable[P, Generator[Result[T, E], T | None, T]] | Generator[Result[T, E], T | None, T],
) -> Callable[P, Result[T, E]] | Result[T, E]:
  """
  Dual-purpose function for emulating do-notation with Result types.

  Use as a decorator for functions that yield Results, or as a helper for generators.
  Essential for imperative-style Result handling. Avoid when simple chaining suffices.
  Can be used as a decorator or called directly with a generator instance.

  ```
  @do
  def my_func() -> Generator[...]:
      x = yield Ok(2)
      y = yield Ok(3)
      return x + y

  my_func()  # Ok(5)
  ```
  """
  if isinstance(fn_or_gen, Generator):
    return _run_do(cast('Generator[Result[T, E], T | None, T]', fn_or_gen))

  if callable(fn_or_gen):
    fn = fn_or_gen

    @functools.wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, E]:
      gen = fn(*args, **kwargs)
      if not isinstance(gen, Generator):  # type: ignore[reportUnnecessaryIsInstance]
        msg = (
          f'do() decorated function must return a Generator (use `yield` inside). Got {type(gen).__name__!r} instead.'
        )
        raise TypeError(msg)
      return _run_do(gen)

    return wrapper

  raise TypeError('do() must be used as a decorator or called with a generator instance.')


def do_async(
  fn_or_gen: Callable[P, AsyncGenerator[Result[T, E], None]] | AsyncGenerator[Result[T, E], None],
) -> Callable[P, Awaitable[Result[T, E]]] | Awaitable[Result[T, E]]:
  """
  Dual-purpose function for emulating async do-notation with Result types.

  Use as a decorator for async functions that yield Results, or as a helper for async generators.
  Essential for imperative-style async Result handling. Avoid when simple async chaining suffices.
  Can be used as a decorator or called directly with an async generator instance.

  ```
  @do_async
  async def my_func() -> AsyncGenerator[...]:
      x = yield Ok(2)
      y = yield Ok(3)
      return x + y
  ```
  """
  if inspect.isasyncgen(fn_or_gen):
    return _run_do_async(fn_or_gen)

  if callable(fn_or_gen):
    fn = fn_or_gen

    @functools.wraps(fn)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, E]:
      async_gen = fn(*args, **kwargs)
      if not inspect.isasyncgen(async_gen):
        if inspect.iscoroutine(async_gen):
          async_gen.close()
        msg = (
          'do_async() decorated function must return an AsyncGenerator (use `yield` inside). '
          f'Got {type(async_gen).__name__!r} instead.'
        )
        raise TypeError(msg)
      return await _run_do_async(async_gen)

    return wrapper

  raise TypeError('do_async() must be used as a decorator or called with an async generator.')


def catch(
  *exceptions: type[BE],
) -> Callable[[Callable[P, T]], Callable[P, Result[T, BE]]]:
  """Deprecated alias for :func:`as_result`.

  Use :func:`as_result` instead.
  """
  _validate_exception_types(exceptions, 'catch')
  warnings.warn('catch() is deprecated, use as_result() instead', DeprecationWarning, stacklevel=2)
  return as_result(*exceptions)


def catch_async(
  *exceptions: type[BE],
) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[Result[T, BE]]]]:
  """Deprecated alias for :func:`as_async_result`.

  Use :func:`as_async_result` instead.
  """
  _validate_exception_types(exceptions, 'catch_async')
  warnings.warn('catch_async() is deprecated, use as_async_result() instead', DeprecationWarning, stacklevel=2)
  return as_async_result(*exceptions)


def _run_do(gen: Generator[Result[T, E], T | None, T]) -> Result[T, E]:
  value: T | None = None
  last_ok_result: Result[T, E] | None = None
  try:
    while True:
      res = gen.send(value)
      if isinstance(res, Err):
        return res
      last_ok_result = res
      value = res.unwrap()
  except StopIteration as e:
    if e.args:
      return Ok(e.args[0])
    if last_ok_result is not None:
      return last_ok_result
    return Ok(cast('T', None))


async def _run_do_async(gen: AsyncGenerator[Result[T, E], T | None]) -> Result[T, E]:
  value: T | None = None
  last_ok_result: Result[T, E] | None = None
  try:
    while True:
      res = await gen.asend(value)
      if isinstance(res, Err):
        return res
      value = res.unwrap()
      last_ok_result = res
  except StopAsyncIteration as e:
    if e.args:
      return Ok(e.args[0])
    if last_ok_result is not None:
      return last_ok_result
    return Ok(cast('T', None))
