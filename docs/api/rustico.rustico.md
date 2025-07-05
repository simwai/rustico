<!-- markdownlint-disable -->

<a href="..\..\src\rustico\rustico.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `rustico.rustico`




**Global Variables**
---------------
- **OkErr**

---

<a href="..\..\src\rustico\rustico.py#L879"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `as_result`

```python
as_result(
    *exceptions: 'type[TBE]'
) → Callable[[Callable[, R]], Callable[, Result[R, TBE]]]
```

Decorator that converts a function to return Result, catching specified exceptions as Err. 

Use when you want to convert exception-based APIs to Result-based APIs. Essential for integrating with existing codebases. Avoid when functions already return Results. 

```
@as_result(ValueError)
def parse_int(x: str) -> int:
     return int(x)

parse_int("42")  # Ok(42)
parse_int("fail")  # Err(ValueError(...))
``` 


---

<a href="..\..\src\rustico\rustico.py#L915"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `as_async_result`

```python
as_async_result(
    *exceptions: 'type[TBE]'
) → Callable[[Callable[, Awaitable[R]]], Callable[, Awaitable[Result[R, TBE]]]]
```

Decorator that converts an async function to return Result, catching specified exceptions as Err. 

Use when you want to convert async exception-based APIs to Result-based APIs. Essential for integrating async codebases. Avoid when async functions already return Results. 

```
@as_async_result(ValueError)
async def parse_int_async(x: str) -> int:
     return int(x)
``` 


---

<a href="..\..\src\rustico\rustico.py#L950"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `is_ok`

```python
is_ok(result: 'Result[T, E]') → TypeIs[Ok[T]]
```

Type guard that returns True if the result is Ok, providing type narrowing. 

Use for type-safe conditional logic and when you need type narrowing. Essential for type checkers. Prefer result.is_ok() for simple boolean checks. 

```
is_ok(Ok(1))  # True
is_ok(Err("fail"))  # False
``` 


---

<a href="..\..\src\rustico\rustico.py#L965"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `is_err`

```python
is_err(result: 'Result[T, E]') → TypeIs[Err[E]]
```

Type guard that returns True if the result is Err, providing type narrowing. 

Use for type-safe conditional logic and when you need type narrowing. Essential for type checkers. Prefer result.is_err() for simple boolean checks. 

```
is_err(Ok(1))  # False
is_err(Err("fail"))  # True
``` 


---

<a href="..\..\src\rustico\rustico.py#L980"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `match`

```python
match(
    result: 'Result[T, E]',
    ok_handler: 'Callable[[T], R]',
    err_handler: 'Callable[[E], R] | None' = None
) → R | None
```

Pattern match on a Result and apply the appropriate handler function. 

This function provides a functional, explicit alternative to Python's pattern matching syntax, allowing you to handle both success (`Ok`) and error (`Err`) cases with dedicated handler functions. It's especially useful when you want to transform or branch on the contents of a Result without unwrapping it or writing conditional logic. 

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


---

<a href="..\..\src\rustico\rustico.py#L1018"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `do`

```python
do(
    fn_or_gen: 'Callable[, Generator[Result[T, E], T, R]] | Generator[Result[T, E], T, R]'
) → Callable[[], Result[R, E]] | Result[R, E]
```

Dual-purpose function for emulating do-notation with Result types. 

Use as a decorator for functions that yield Results, or as a helper for generators. Essential for imperative-style Result handling. Avoid when simple chaining suffices. Can be used as a decorator or called directly with a generator instance. 

```
@do
def my_func() -> Generator[...]:
     x = yield Ok(2)
     y = yield Ok(3)
     return x + y

my_func()  # Ok(5)
``` 


---

<a href="..\..\src\rustico\rustico.py#L1056"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `do_async`

```python
do_async(
    fn_or_gen: 'Callable[, AsyncGenerator[Result[T, E], None]] | AsyncGenerator[Result[T, E], None]'
) → Callable[, Awaitable[Result[T, E]]] | Awaitable[Result[T, E]]
```

Dual-purpose function for emulating async do-notation with Result types. 

Use as a decorator for async functions that yield Results, or as a helper for async generators. Essential for imperative-style async Result handling. Avoid when simple async chaining suffices. Can be used as a decorator or called directly with an async generator instance. 

```
@do_async
async def my_func() -> AsyncGenerator[...]:
     x = yield Ok(2)
     y = yield Ok(3)
     return x + y
``` 


---

<a href="..\..\src\rustico\rustico.py#L1090"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `catch`

```python
catch(*errors: 'type[E]') → Callable[[Callable[, T]], Callable[, Result[T, E]]]
```

Decorator that catches specified exceptions and returns them as Err Results. 

Use when you want to convert specific exceptions to Results without catching all exceptions. More precise than as_result for targeted exception handling. Avoid when you need to catch all exceptions. 

```
@catch(ValueError)
def parse(x: str) -> int:
     return int(x)
``` 


---

<a href="..\..\src\rustico\rustico.py#L1120"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `catch_async`

```python
catch_async(
    *errors: 'type[E]'
) → Callable[[Callable[, Awaitable[T]]], Callable[, Awaitable[Result[T, E]]]]
```

Decorator that catches specified exceptions in async functions and returns them as Err Results. 

Use when you want to convert specific async exceptions to Results without catching all exceptions. More precise than as_async_result for targeted exception handling. Avoid when you need to catch all exceptions. 

```
@catch_async(ValueError)
async def parse_async(x: str) -> int:
     return int(x)
``` 


---

<a href="..\..\src\rustico\rustico.py#L34"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `UnwrapError`
Exception raised when an unwrap or expect operation fails on a Result. 

```
try:
     Err("fail").unwrap()
except UnwrapError as e:
     print(e)
# Called `Result.unwrap()` on an `Err` value: 'fail'
``` 

<a href="..\..\src\rustico\rustico.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(result: 'Result[object, object]', message: 'str') → None
```






---

#### <kbd>property</kbd> result

Returns the original result that caused the unwrap failure. 

Useful for debugging and error recovery scenarios where you need to inspect the original Result that failed to unwrap. Common in error handling pipelines where you want to log the original error context. 

```
try:
     Err("fail").unwrap()
except UnwrapError as e:
     assert isinstance(e.result, Err)
``` 




---

<a href="..\..\src\rustico\rustico.py#L72"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Ok`
Represents a successful result containing a value. 

Use when operations succeed and you want to chain further operations. Avoid when you need to represent failure states - use Err instead. 

```
Ok(42).unwrap()  # 42
``` 

<a href="..\..\src\rustico\rustico.py#L87"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(value: 'T') → None
```






---

#### <kbd>property</kbd> ok_value

Returns the inner value for pattern matching and direct access. 

Use with match statements and when you need direct property access. Prefer unwrap() for general value extraction. Avoid when error handling is needed. 

```
Ok(2).ok_value  # 2
``` 



---

<a href="..\..\src\rustico\rustico.py#L195"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `alt`

```python
alt(op: 'Callable[[E], F]') → Ok[T]
```

No-op for Ok instances - error transformation doesn't apply to successful results. 

Use in generic code that handles both Ok and Err. The operation is ignored for Ok instances, maintaining the original value. Avoid when you know the Result is Ok. 

```
Ok(1).alt(lambda e: 0)  # Ok(1)
``` 

---

<a href="..\..\src\rustico\rustico.py#L372"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `and_then`

```python
and_then(op: 'Callable[[T], Result[U, E]]') → Result[U, E]
```

Chains another Result-returning operation on the contained value (monadic bind). 

Use for chaining operations that can fail, creating pipelines of fallible computations. Essential for functional error handling. Avoid when the operation cannot fail. 

```
Ok(2).and_then(lambda x: Ok(x * 2))  # Ok(4)
``` 

---

<a href="..\..\src\rustico\rustico.py#L385"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `and_then_async`

```python
and_then_async(op: 'Callable[[T], Awaitable[Result[U, E]]]') → Result[U, E]
```

Asynchronously chains another Result-returning operation on the contained value. 

Use for chaining async operations that can fail. Essential for async functional error handling patterns. Avoid when the async operation cannot fail. 

```
await Ok(2).and_then_async(async_lambda)
``` 

---

<a href="..\..\src\rustico\rustico.py#L141"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `err`

```python
err() → None
```

Always returns None for Ok instances since there's no error. 

Use for symmetry with Err.err() in generic code. Avoid when you know the Result is Ok - the return will always be None. 

```
Ok(1).err()  # None
``` 

---

<a href="..\..\src\rustico\rustico.py#L208"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expect`

```python
expect(_message: 'str') → T
```

Returns the contained value, ignoring the message since Ok cannot fail. 

Use when you want consistent API with Err.expect() in generic code. Prefer unwrap() when you know the Result is Ok. Avoid when error context isn't needed. 

```
Ok(1).expect("should not fail")  # 1
``` 

---

<a href="..\..\src\rustico\rustico.py#L221"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expect_err`

```python
expect_err(message: 'str') → NoReturn
```

Always raises UnwrapError since Ok instances don't contain errors. 

Use when you expect an error but got success - indicates a logic error. Common in testing scenarios. Avoid in normal business logic. 

```
try:
     Ok(1).expect_err("should be error")
except UnwrapError:
     pass
``` 

---

<a href="..\..\src\rustico\rustico.py#L411"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `inspect`

```python
inspect(op: 'Callable[[T], Any]') → Result[T, E]
```

Calls the provided function with the contained value for side effects, returns self. 

Use for debugging, logging, or other side effects without changing the Result. Common for tracing successful values in pipelines. Avoid when side effects are expensive. 

```
Ok(2).inspect(print)  # prints 2, returns Ok(2)
``` 

---

<a href="..\..\src\rustico\rustico.py#L425"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `inspect_err`

```python
inspect_err(op: 'Callable[[E], Any]') → Result[T, E]
```

No-op for Ok instances - error inspection doesn't apply to successful results. 

Use in generic code that handles both Ok and Err. The operation is ignored for Ok instances. Avoid when you know the Result is Ok. 

```
Ok(2).inspect_err(print)  # Ok(2), nothing printed
``` 

---

<a href="..\..\src\rustico\rustico.py#L115"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_err`

```python
is_err() → Literal[False]
```

Always returns False for Ok instances. 

Use for type narrowing and conditional logic. Prefer this over isinstance checks for better type inference. Avoid when you already know the Result type. 

```
Ok(1).is_err()  # False
``` 

---

<a href="..\..\src\rustico\rustico.py#L102"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_ok`

```python
is_ok() → Literal[True]
```

Always returns True for Ok instances. 

Use for type narrowing and conditional logic. Prefer this over isinstance checks for better type inference. Avoid when you already know the Result type. 

```
Ok(1).is_ok()  # True
``` 

---

<a href="..\..\src\rustico\rustico.py#L305"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map`

```python
map(op: 'Callable[[T], U]') → Ok[U]
```

Transforms the contained value using the provided function, wrapping result in Ok. 

Use for transforming successful values while preserving the Ok context. Essential for functional programming patterns. Avoid when transformation can fail without proper error handling. 

```
Ok(2).map(lambda x: x * 10)  # Ok(20)
``` 

---

<a href="..\..\src\rustico\rustico.py#L319"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_async`

```python
map_async(op: 'Callable[[T], Awaitable[U]]') → Ok[U]
```

Asynchronously transforms the contained value, wrapping result in Ok. 

Use for async transformations of successful values. Essential for async functional programming patterns. Avoid when the async operation can fail without proper error handling. 

```
await Ok(2).map_async(async_lambda)
``` 

---

<a href="..\..\src\rustico\rustico.py#L359"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_err`

```python
map_err(op: 'Callable[[E], F]') → Ok[T]
```

No-op for Ok instances - error transformation doesn't apply to successful results. 

Use in generic code that handles both Ok and Err. The operation is ignored for Ok instances, maintaining the original value. Avoid when you know the Result is Ok. 

```
Ok(2).map_err(lambda e: 0)  # Ok(2)
``` 

---

<a href="..\..\src\rustico\rustico.py#L333"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_or`

```python
map_or(default: 'U', op: 'Callable[[T], U]') → U
```

Transforms the contained value using the operation, ignoring the default. 

Use when you want consistent API with Err.map_or() in generic code. The default is never used for Ok instances. Prefer map() when you know the Result is Ok. 

```
Ok(2).map_or(0, lambda x: x * 2)  # 4
``` 

---

<a href="..\..\src\rustico\rustico.py#L346"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_or_else`

```python
map_or_else(default_op: 'Callable[[], U]', op: 'Callable[[T], U]') → U
```

Transforms the contained value using the operation, ignoring the default operation. 

Use when you want consistent API with Err.map_or_else() in generic code. The default operation is never called for Ok instances. Prefer map() when you know the Result is Ok. 

```
Ok(2).map_or_else(lambda: 0, lambda x: x * 2)  # 4
``` 

---

<a href="..\..\src\rustico\rustico.py#L438"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `match`

```python
match(
    ok: 'Callable[[T], U] | None' = None,
    err: 'Callable[[E], U] | None' = None
) → U
```

Pattern matches on Ok, requiring an 'ok' handler and ignoring 'err' handler. 

Use for exhaustive pattern matching with clear intent. Provides type safety and forces explicit handling. Avoid when simple unwrap() or map() suffices. 

```
Ok(1).match(ok=lambda x: f"Got {x}", err=lambda e: f"Error: {e}")  # 'Got 1'
``` 

---

<a href="..\..\src\rustico\rustico.py#L128"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ok`

```python
ok() → T
```

Returns the contained value for Ok instances. 

Use when you want to extract the value without unwrapping. Prefer unwrap() when you're certain the Result is Ok. Avoid when you need error handling. 

```
Ok(1).ok()  # 1
``` 

---

<a href="..\..\src\rustico\rustico.py#L398"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `or_else`

```python
or_else(op: 'Callable[[E], Result[T, F]]') → Ok[T]
```

No-op for Ok instances - error recovery doesn't apply to successful results. 

Use in generic code that handles both Ok and Err. The operation is ignored for Ok instances, maintaining the original value. Avoid when you know the Result is Ok. 

```
Ok(2).or_else(lambda e: Ok(0))  # Ok(2)
``` 

---

<a href="..\..\src\rustico\rustico.py#L168"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `swap`

```python
swap() → Err[T]
```

Converts Ok to Err with the same value, swapping success/failure semantics. 

Use when you need to invert the meaning of success/failure in your logic. Common in testing scenarios or when adapting between different Result conventions. Avoid in normal business logic where semantics should remain consistent. 

```
Ok("x").swap()  # Err('x')
``` 

---

<a href="..\..\src\rustico\rustico.py#L237"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap`

```python
unwrap() → T
```

Returns the contained value safely since Ok instances always contain values. 

Use when you're certain the Result is Ok or when you want to fail fast on errors. Prefer this over ok() for value extraction. Avoid when error handling is required. 

```
Ok(1).unwrap()  # 1
``` 

---

<a href="..\..\src\rustico\rustico.py#L250"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_err`

```python
unwrap_err() → NoReturn
```

Always raises UnwrapError since Ok instances don't contain errors. 

Use when you expect an error but got success - indicates a logic error. Common in testing scenarios. Avoid in normal business logic. 

```
try:
     Ok(1).unwrap_err()
except UnwrapError:
     pass
``` 

---

<a href="..\..\src\rustico\rustico.py#L266"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or`

```python
unwrap_or(_default: 'U') → T
```

Returns the contained value, ignoring the default since Ok always has a value. 

Use when you want consistent API with Err.unwrap_or() in generic code. Prefer unwrap() when you know the Result is Ok. Avoid when the default is expensive. 

```
Ok(1).unwrap_or(0)  # 1
``` 

---

<a href="..\..\src\rustico\rustico.py#L279"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or_else`

```python
unwrap_or_else(op: 'Callable[[E], T]') → T
```

Returns the contained value, ignoring the operation since Ok always has a value. 

Use when you want consistent API with Err.unwrap_or_else() in generic code. The operation is never called for Ok instances. Avoid when you know the Result is Ok. 

```
Ok(1).unwrap_or_else(lambda e: 0)  # 1
``` 

---

<a href="..\..\src\rustico\rustico.py#L292"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or_raise`

```python
unwrap_or_raise(e: 'object') → T
```

Returns the contained value, ignoring the exception since Ok cannot fail. 

Use when you want consistent API with Err.unwrap_or_raise() in generic code. The exception is never raised for Ok instances. Avoid when you know the Result is Ok. 

```
Ok(1).unwrap_or_raise(Exception)  # 1
``` 

---

<a href="..\..\src\rustico\rustico.py#L182"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `value_or`

```python
value_or(default: 'Any') → T
```

Returns the contained value, ignoring the default (alias for unwrap_or). 

Use when you want consistent API with Err.value_or(). Prefer unwrap() when you know the Result is Ok. Avoid when the default value is expensive to compute. 

```
Ok(42).value_or(0)  # 42
``` 


---

<a href="..\..\src\rustico\rustico.py#L454"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Err`
Represents a failed result containing an error value. 

Use when operations fail and you want to propagate error information. Avoid when success is the only meaningful outcome. 

```
Err("fail").unwrap_or(0)  # 0
``` 

<a href="..\..\src\rustico\rustico.py#L469"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(value: 'E') → None
```






---

#### <kbd>property</kbd> err_value

Returns the inner error value for pattern matching and direct access. 

Use with match statements and when you need direct property access. Prefer unwrap_err() for general error extraction. Avoid when success handling is needed. 

```
Err("fail").err_value  # "fail"
``` 

---

#### <kbd>property</kbd> trace

Returns the captured stack trace as a list of formatted strings for BaseException errors. 

Use for debugging and error reporting when the error value is an exception. Computed lazily to avoid performance overhead. Returns None for non-exception errors. Avoid when error value is not an exception. 

```
try:
     raise ValueError("fail")
except ValueError as e:
     err = Err(e)
     print(err.trace)
``` 



---

<a href="..\..\src\rustico\rustico.py#L608"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `alt`

```python
alt(op: 'Callable[[E], F]') → Err[F]
```

Transforms the contained error value using the provided function, wrapping result in Err. 

Use for transforming error values while preserving the Err context. Common for error normalization and enrichment. Avoid when error transformation can fail without proper handling. 

```
Err(1).alt(lambda e: e + 1)  # Err(2)
``` 

---

<a href="..\..\src\rustico\rustico.py#L793"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `and_then`

```python
and_then(op: 'Callable[[T], Result[U, E]]') → Err[E]
```

No-op for Err instances - chaining operations doesn't apply to failed results. 

Use in generic code that handles both Ok and Err. The operation is ignored for Err instances, maintaining the original error. Avoid when you know the Result is Err. 

```
Err("fail").and_then(lambda x: Ok(x * 2))  # Err('fail')
``` 

---

<a href="..\..\src\rustico\rustico.py#L806"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `and_then_async`

```python
and_then_async(op: 'Callable[[T], Awaitable[Result[U, E]]]') → Err[E]
```

No-op for Err instances - async chaining operations doesn't apply to failed results. 

Use in generic code that handles both Ok and Err. The operation is ignored for Err instances, maintaining the original error. Avoid when you know the Result is Err. 

```
await Err("fail").and_then_async(lambda x: Ok(x * 2))  # Err('fail')
``` 

---

<a href="..\..\src\rustico\rustico.py#L554"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `err`

```python
err() → E
```

Returns the contained error value for Err instances. 

Use when you want to extract the error without unwrapping. Prefer unwrap_err() when you're certain the Result is Err. Avoid when you need success handling. 

```
Err("fail").err()  # "fail"
``` 

---

<a href="..\..\src\rustico\rustico.py#L622"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expect`

```python
expect(message: 'str') → NoReturn
```

Always raises UnwrapError with the provided message since Err instances represent failure. 

Use when you expect success but got failure - provides clear error context. Common for assertions and fail-fast scenarios. Avoid in normal error handling. 

```
try:
     Err("fail").expect("should not fail")
except UnwrapError:
     pass
``` 

---

<a href="..\..\src\rustico\rustico.py#L641"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expect_err`

```python
expect_err(_message: 'str') → E
```

Returns the contained error value, ignoring the message since Err always contains errors. 

Use when you want consistent API with Ok.expect_err() in generic code. Prefer unwrap_err() when you know the Result is Err. Avoid when success context isn't needed. 

```
Err("fail").expect_err("should be error")  # "fail"
``` 

---

<a href="..\..\src\rustico\rustico.py#L832"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `inspect`

```python
inspect(op: 'Callable[[T], Any]') → Result[T, E]
```

No-op for Err instances - value inspection doesn't apply to failed results. 

Use in generic code that handles both Ok and Err. The operation is ignored for Err instances. Avoid when you know the Result is Err. 

```
Err("fail").inspect(print)  # Err('fail'), nothing printed
``` 

---

<a href="..\..\src\rustico\rustico.py#L845"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `inspect_err`

```python
inspect_err(op: 'Callable[[E], Any]') → Result[T, E]
```

Calls the provided function with the contained error value for side effects, returns self. 

Use for debugging, logging, or other side effects without changing the Result. Common for tracing error values in pipelines. Avoid when side effects are expensive. 

```
Err("fail").inspect_err(print)  # prints 'fail', returns Err('fail')
``` 

---

<a href="..\..\src\rustico\rustico.py#L528"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_err`

```python
is_err() → Literal[True]
```

Always returns True for Err instances. 

Use for type narrowing and conditional logic. Prefer this over isinstance checks for better type inference. Avoid when you already know the Result type. 

```
Err("fail").is_err()  # True
``` 

---

<a href="..\..\src\rustico\rustico.py#L515"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_ok`

```python
is_ok() → Literal[False]
```

Always returns False for Err instances. 

Use for type narrowing and conditional logic. Prefer this over isinstance checks for better type inference. Avoid when you already know the Result type. 

```
Err("fail").is_ok()  # False
``` 

---

<a href="..\..\src\rustico\rustico.py#L728"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map`

```python
map(op: 'Callable[[T], U]') → Err[E]
```

No-op for Err instances - value transformation doesn't apply to failed results. 

Use in generic code that handles both Ok and Err. The operation is ignored for Err instances, maintaining the original error. Avoid when you know the Result is Err. 

```
Err("fail").map(lambda x: x * 2)  # Err('fail')
``` 

---

<a href="..\..\src\rustico\rustico.py#L741"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_async`

```python
map_async(op: 'Callable[[T], Awaitable[U]]') → Err[E]
```

No-op for Err instances - async value transformation doesn't apply to failed results. 

Use in generic code that handles both Ok and Err. The operation is ignored for Err instances, maintaining the original error. Avoid when you know the Result is Err. 

```
await Err("fail").map_async(lambda x: x * 2)  # Err('fail')
``` 

---

<a href="..\..\src\rustico\rustico.py#L780"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_err`

```python
map_err(op: 'Callable[[E], F]') → Err[F]
```

Transforms the contained error value using the provided function, wrapping result in Err. 

Use for transforming error values while preserving the Err context. Common for error normalization and enrichment. Avoid when error transformation can fail. 

```
Err(2).map_err(lambda e: e + 1)  # Err(3)
``` 

---

<a href="..\..\src\rustico\rustico.py#L754"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_or`

```python
map_or(default: 'U', op: 'Callable[[T], U]') → U
```

Returns the default value since Err instances don't contain success values to transform. 

Use when you want to provide a fallback value instead of transforming. The operation is ignored for Err instances. Avoid when the default is expensive. 

```
Err("fail").map_or(0, lambda x: x * 2)  # 0
``` 

---

<a href="..\..\src\rustico\rustico.py#L767"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_or_else`

```python
map_or_else(default_op: 'Callable[[], U]', op: 'Callable[[E], U]') → U
```

Calls the default operation since Err instances don't contain success values to transform. 

Use when you want to compute a fallback value for failed results. The main operation is ignored for Err instances. Avoid when the default operation is expensive. 

```
Err("fail").map_or_else(lambda: 42, lambda x: x * 2)  # 42
``` 

---

<a href="..\..\src\rustico\rustico.py#L859"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `match`

```python
match(
    ok: 'Callable[[T], U] | None' = None,
    err: 'Callable[[E], U] | None' = None
) → U
```

Pattern matches on Err, requiring an 'err' handler and ignoring 'ok' handler. 

Use for exhaustive pattern matching with clear intent. Provides type safety and forces explicit handling. Avoid when simple unwrap_err() or map_err() suffices. 

```
Err("fail").match(ok=lambda x: f"Got {x}", err=lambda e: f"Error: {e}")  # 'Error: fail'
``` 

---

<a href="..\..\src\rustico\rustico.py#L541"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ok`

```python
ok() → None
```

Always returns None for Err instances since there's no success value. 

Use for symmetry with Ok.ok() in generic code. Avoid when you know the Result is Err - the return will always be None. 

```
Err("fail").ok()  # None
``` 

---

<a href="..\..\src\rustico\rustico.py#L819"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `or_else`

```python
or_else(op: 'Callable[[E], Result[T, F]]') → Result[T, F]
```

Applies error recovery operation to the contained error value (monadic bind for errors). 

Use for chaining error recovery operations, creating pipelines of error handling. Essential for functional error recovery patterns. Avoid when the operation cannot fail. 

```
Err(2).or_else(lambda e: Ok(e + 1))  # Ok(3)
``` 

---

<a href="..\..\src\rustico\rustico.py#L581"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `swap`

```python
swap() → Ok[E]
```

Converts Err to Ok with the error value, swapping failure/success semantics. 

Use when you need to invert the meaning of success/failure in your logic. Common in testing scenarios or when adapting between different Result conventions. Avoid in normal business logic where semantics should remain consistent. 

```
Err("fail").swap()  # Ok('fail')
``` 

---

<a href="..\..\src\rustico\rustico.py#L654"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap`

```python
unwrap() → NoReturn
```

Always raises UnwrapError since Err instances don't contain success values. 

Use when you expect success but got failure - indicates a logic error. Common for fail-fast scenarios and debugging. Avoid in normal error handling. 

```
try:
     Err("fail").unwrap()
except UnwrapError:
     pass
``` 

---

<a href="..\..\src\rustico\rustico.py#L673"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_err`

```python
unwrap_err() → E
```

Returns the contained error value safely since Err instances always contain errors. 

Use when you're certain the Result is Err or when you want to fail fast on success. Prefer this over err() for error extraction. Avoid when success handling is required. 

```
Err("fail").unwrap_err()  # "fail"
``` 

---

<a href="..\..\src\rustico\rustico.py#L686"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or`

```python
unwrap_or(default: 'U') → U
```

Returns the default value since Err instances don't contain success values. 

Use when you want to provide a fallback value for failed operations. Essential for graceful degradation patterns. Avoid when the default is expensive to compute. 

```
Err("fail").unwrap_or(0)  # 0
``` 

---

<a href="..\..\src\rustico\rustico.py#L699"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or_else`

```python
unwrap_or_else(op: 'Callable[[E], T]') → T
```

Applies the operation to the error value and returns the result. 

Use when you want to compute a fallback value based on the error. Essential for error recovery patterns. Avoid when the operation is expensive or can fail. 

```
Err(2).unwrap_or_else(lambda e: e + 1)  # 3
``` 

---

<a href="..\..\src\rustico\rustico.py#L712"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or_raise`

```python
unwrap_or_raise(e: 'type[TBE]') → NoReturn
```

Raises the provided exception type with the error value as the message. 

Use when you want to convert Result errors to traditional exceptions. Common at API boundaries. Avoid when you want to maintain Result-based error handling. 

```
try:
     Err("fail").unwrap_or_raise(ValueError)
except ValueError:
     pass
``` 

---

<a href="..\..\src\rustico\rustico.py#L595"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `value_or`

```python
value_or(default: 'U') → U
```

Returns the default value since Err instances don't contain success values. 

Use when you want to provide a fallback value for failed operations. Essential for graceful degradation patterns. Avoid when the default is expensive to compute. 

```
Err("fail").value_or(0)  # 0
``` 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
