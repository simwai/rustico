<!-- markdownlint-disable -->

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `rustico`




**Global Variables**
---------------
- **TYPE_CHECKING**

---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L408"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `as_result`

```python
as_result(
    *exceptions: 'type[BE]'
) → Callable[[Callable[P, T]], Callable[P, Result[T, BE]]]
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

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L441"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `as_async_result`

```python
as_async_result(
    *exceptions: 'type[BE]'
) → Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[Result[T, BE]]]]
```

Decorator that converts an async function to return Result, catching specified exceptions as Err. 

Use when you want to convert async exception-based APIs to Result-based APIs. Essential for integrating async codebases. Avoid when async functions already return Results. 

```
@as_async_result(ValueError)
async def parse_int_async(x: str) -> int:
     return int(x)
``` 


---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L473"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `is_ok`

```python
is_ok(result: 'Result[T, E]') → TypeIs[Ok[T, E]]
```

Type guard that returns True if the result is Ok, providing type narrowing. 

Use for type-safe conditional logic and when you need type narrowing. Essential for type checkers. Prefer result.is_ok() for simple boolean checks. 

```
is_ok(Ok(1))  # True
is_ok(Err("fail"))  # False
``` 


---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L488"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `is_err`

```python
is_err(result: 'Result[T, E]') → TypeIs[Err[T, E]]
```

Type guard that returns True if the result is Err, providing type narrowing. 

Use for type-safe conditional logic and when you need type narrowing. Essential for type checkers. Prefer result.is_err() for simple boolean checks. 

```
is_err(Ok(1))  # False
is_err(Err("fail"))  # True
``` 


---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L503"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `match`

```python
match(
    result: 'Result[T, E]',
    ok_handler: 'Callable[[T], R]',
    err_handler: 'Callable[[E], R] | None' = None
) → R | None
```

**Deprecated:** Use `result.match(ok=..., err=...)` instead. 

This function is deprecated and has been removed in v2.0. 

 Pattern match on a Result and apply the appropriate handler function. 

 This function provides a functional, explicit alternative to Python's pattern matching syntax,  allowing you to handle both success (`Ok`) and error (`Err`) cases with dedicated handler functions.  It's especially useful when you want to transform or branch on the contents of a Result  without unwrapping it or writing conditional logic. 

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

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L550"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `do`

```python
do(
    fn_or_gen: 'Callable[P, Generator[Result[T, E], T | None, T]] | Generator[Result[T, E], T | None, T]'
) → Callable[P, Result[T, E]] | Result[T, E]
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

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L591"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `do_async`

```python
do_async(
    fn_or_gen: 'Callable[P, AsyncGenerator[Result[T, E], None]] | AsyncGenerator[Result[T, E], None]'
) → Callable[P, Awaitable[Result[T, E]]] | Awaitable[Result[T, E]]
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

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L633"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `catch`

```python
catch(
    *exceptions: 'type[BE]'
) → Callable[[Callable[P, T]], Callable[P, Result[T, BE]]]
```

Decorator that catches specified exceptions and returns them as Err Results. 

Use when you want to convert specific exceptions to Results without catching all exceptions. More precise than as_result for targeted exception handling. Avoid when you need to catch all exceptions. 

```
@catch(ValueError)
def parse(x: str) -> int:
     return int(x)
``` 


---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L664"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `catch_async`

```python
catch_async(
    *exceptions: 'type[BE]'
) → Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[Result[T, BE]]]]
```

Decorator that catches specified exceptions in async functions and returns them as Err Results. 

Use when you want to convert specific async exceptions to Results without catching all exceptions. More precise than as_async_result for targeted exception handling. Avoid when you need to catch all exceptions. 

```
@catch_async(ValueError)
async def parse_async(x: str) -> int:
     return int(x)
``` 


---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L34"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Result`
Base class for Ok (success) and Err (failure) variants. 

Use this for isinstance checks instead of the deprecated OkErr tuple. Use Ok/Err methods directly for type-specific functionality. 

```
isinstance(Ok(42), Result)  # True
isinstance(Err("fail"), Result)  # True
``` 




---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L102"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `alt`

```python
alt(op: 'Callable[[E], F]') → Result[T, F]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L87"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `and_then`

```python
and_then(op: 'Callable[[T], Result[U, E]]') → Result[U, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L117"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `and_then_async`

```python
and_then_async(op: 'Callable[[T], Awaitable[Result[U, E]]]') → Result[U, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L57"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `err`

```python
err() → E | None
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L66"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expect`

```python
expect(message: 'str') → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expect_err`

```python
expect_err(message: 'str') → E
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L93"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `inspect`

```python
inspect(op: 'Callable[[T], Any]') → Result[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L96"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `inspect_err`

```python
inspect_err(op: 'Callable[[E], Any]') → Result[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L51"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_err`

```python
is_err() → bool
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L48"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_ok`

```python
is_ok() → bool
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L81"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map`

```python
map(op: 'Callable[[T], U]') → Result[U, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L114"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_async`

```python
map_async(op: 'Callable[[T], Awaitable[U]]') → Result[U, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L84"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_err`

```python
map_err(op: 'Callable[[E], F]') → Result[T, F]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L105"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_or`

```python
map_or(default: 'U', op: 'Callable[[T], U]') → U
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L108"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_or_else`

```python
map_or_else(default_op: 'Callable[[], U]', op: 'Callable[[T], U]') → U
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L99"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `match`

```python
match(
    ok: 'Callable[[T], U] | None' = None,
    err: 'Callable[[E], U] | None' = None
) → U
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L54"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ok`

```python
ok() → T | None
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L90"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `or_else`

```python
or_else(op: 'Callable[[E], Result[T, F]]') → Result[T, F]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L60"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap`

```python
unwrap() → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_err`

```python
unwrap_err() → E
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L75"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or`

```python
unwrap_or(default: 'T') → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L78"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or_else`

```python
unwrap_or_else(op: 'Callable[[E], T]') → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L111"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or_raise`

```python
unwrap_or_raise(exception_type: 'type[BaseException]') → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L72"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `value_or`

```python
value_or(default: 'T') → T
```






---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L121"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `UnwrapError`
Exception raised when an unwrap or expect operation fails on a Result. 

```
try:
     Err("fail").unwrap()
except UnwrapError as e:
     print(e)
# Called `Result.unwrap()` on an `Err` value: 'fail'
``` 

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L136"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(result: 'Result[T, E]', message: 'str') → None
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

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L163"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Ok`
Represents a successful result containing a value. 

Use when operations succeed and you want to chain further operations. Avoid when you need to represent failure states - use Err instead. 

```
Ok(42).unwrap()  # 42
``` 

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L178"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(value: 'T') → None
```






---

#### <kbd>property</kbd> ok_value







---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L212"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `alt`

```python
alt(op: 'Callable[[E], F]') → Ok[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L251"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `and_then`

```python
and_then(op: 'Callable[[T], Result[U, E]]') → Result[U, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L254"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `and_then_async`

```python
and_then_async(op: 'Callable[[T], Awaitable[Result[U, E]]]') → Result[U, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L202"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `err`

```python
err() → None
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L215"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expect`

```python
expect(message: 'str') → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L218"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expect_err`

```python
expect_err(message: 'str') → NoReturn
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L260"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `inspect`

```python
inspect(op: 'Callable[[T], Any]') → Ok[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L264"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `inspect_err`

```python
inspect_err(op: 'Callable[[E], Any]') → Ok[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L196"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_err`

```python
is_err() → Literal[False]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L193"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_ok`

```python
is_ok() → Literal[True]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L236"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map`

```python
map(op: 'Callable[[T], U]') → Ok[U, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L239"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_async`

```python
map_async(op: 'Callable[[T], Awaitable[U]]') → Ok[U, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L248"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_err`

```python
map_err(op: 'Callable[[E], F]') → Ok[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L242"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_or`

```python
map_or(default: 'U', op: 'Callable[[T], U]') → U
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L245"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_or_else`

```python
map_or_else(default_op: 'Callable[[], U]', op: 'Callable[[T], U]') → U
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L267"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `match`

```python
match(
    ok: 'Callable[[T], U] | None' = None,
    err: 'Callable[[E], U] | None' = None
) → U
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L199"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ok`

```python
ok() → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L257"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `or_else`

```python
or_else(op: 'Callable[[E], Result[T, F]]') → Ok[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L221"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap`

```python
unwrap() → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L224"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_err`

```python
unwrap_err() → NoReturn
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L227"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or`

```python
unwrap_or(default: 'T') → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L230"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or_else`

```python
unwrap_or_else(op: 'Callable[[E], T]') → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L233"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or_raise`

```python
unwrap_or_raise(exception_type: 'type[BaseException]') → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L209"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `value_or`

```python
value_or(default: 'T') → T
```






---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L273"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Err`
Represents a failed result containing an error value. 

Use when operations fail and you want to propagate error information. Avoid when success is the only meaningful outcome. 

```
Err("fail").unwrap_or(0)  # 0
``` 

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L288"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(value: 'E') → None
```






---

#### <kbd>property</kbd> err_value





---

#### <kbd>property</kbd> trace







---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L335"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `alt`

```python
alt(op: 'Callable[[E], F]') → Result[T, F]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L380"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `and_then`

```python
and_then(op: 'Callable[[T], Result[U, E]]') → Err[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L383"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `and_then_async`

```python
and_then_async(op: 'Callable[[T], Awaitable[Result[U, E]]]') → Err[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L325"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `err`

```python
err() → E
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L338"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expect`

```python
expect(message: 'str') → NoReturn
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L344"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expect_err`

```python
expect_err(message: 'str') → E
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L389"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `inspect`

```python
inspect(op: 'Callable[[T], Any]') → Err[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L392"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `inspect_err`

```python
inspect_err(op: 'Callable[[E], Any]') → Err[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L319"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_err`

```python
is_err() → Literal[True]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L316"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_ok`

```python
is_ok() → Literal[False]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L365"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map`

```python
map(op: 'Callable[[T], U]') → Err[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L368"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_async`

```python
map_async(op: 'Callable[[T], Awaitable[U]]') → Err[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L377"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_err`

```python
map_err(op: 'Callable[[E], F]') → Err[T, F]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L371"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_or`

```python
map_or(default: 'U', op: 'Callable[[T], U]') → U
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L374"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_or_else`

```python
map_or_else(default_op: 'Callable[[], U]', op: 'Callable[[T], U]') → U
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L396"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `match`

```python
match(
    ok: 'Callable[[T], U] | None' = None,
    err: 'Callable[[E], U] | None' = None
) → U
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L322"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ok`

```python
ok() → None
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L386"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `or_else`

```python
or_else(op: 'Callable[[E], Result[T, F]]') → Result[T, F]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L347"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap`

```python
unwrap() → NoReturn
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L353"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_err`

```python
unwrap_err() → E
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L356"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or`

```python
unwrap_or(default: 'T') → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L359"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or_else`

```python
unwrap_or_else(op: 'Callable[[E], T]') → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L362"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or_raise`

```python
unwrap_or_raise(exception_type: 'type[BaseException]') → NoReturn
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L332"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `value_or`

```python
value_or(default: 'T') → T
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
