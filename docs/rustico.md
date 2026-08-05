<!-- markdownlint-disable -->

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `rustico`




**Global Variables**
---------------
- **TYPE_CHECKING**

---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L414"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L447"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L479"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L494"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L509"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `match`

```python
match(
    result: 'Result[T, E]',
    ok_handler: 'Callable[[T], R]',
    err_handler: 'Callable[[E], R] | None' = None
) → R | None
```

**Deprecated:** Use `result.match(ok=..., err=...)` instead. 

This function is deprecated but remains available for backward compatibility. 

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

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L556"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L597"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L639"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `catch`

```python
catch(
    *exceptions: 'type[BE]'
) → Callable[[Callable[P, T]], Callable[P, Result[T, BE]]]
```

Deprecated alias for :func:`as_result`. 

Use :func:`as_result` instead. 


---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L651"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `catch_async`

```python
catch_async(
    *exceptions: 'type[BE]'
) → Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[Result[T, BE]]]]
```

Deprecated alias for :func:`as_async_result`. 

Use :func:`as_async_result` instead. 


---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Result`
Base class for Ok (success) and Err (failure) variants. 

Use this for isinstance checks instead of the deprecated OkErr tuple. Use Ok/Err methods directly for type-specific functionality. 

```
isinstance(Ok(42), Result)  # True
isinstance(Err("fail"), Result)  # True
``` 




---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L100"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `alt`

```python
alt(op: 'Callable[[E], F]') → Result[T, F]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L85"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `and_then`

```python
and_then(op: 'Callable[[T], Result[U, E]]') → Result[U, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L115"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `and_then_async`

```python
and_then_async(op: 'Callable[[T], Awaitable[Result[U, E]]]') → Result[U, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `err`

```python
err() → E | None
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L64"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expect`

```python
expect(message: 'str') → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L67"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expect_err`

```python
expect_err(message: 'str') → E
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L91"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `inspect`

```python
inspect(op: 'Callable[[T], Any]') → Result[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `inspect_err`

```python
inspect_err(op: 'Callable[[E], Any]') → Result[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_err`

```python
is_err() → bool
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L46"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_ok`

```python
is_ok() → bool
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L79"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map`

```python
map(op: 'Callable[[T], U]') → Result[U, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L112"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_async`

```python
map_async(op: 'Callable[[T], Awaitable[U]]') → Result[U, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L82"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_err`

```python
map_err(op: 'Callable[[E], F]') → Result[T, F]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L103"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_or`

```python
map_or(default: 'U', op: 'Callable[[T], U]') → U
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L106"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_or_else`

```python
map_or_else(default_op: 'Callable[[], U]', op: 'Callable[[T], U]') → U
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L97"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `match`

```python
match(
    ok: 'Callable[[T], U] | None' = None,
    err: 'Callable[[E], U] | None' = None
) → U
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L52"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ok`

```python
ok() → T | None
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L88"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `or_else`

```python
or_else(op: 'Callable[[E], Result[T, F]]') → Result[T, F]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L58"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap`

```python
unwrap() → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_err`

```python
unwrap_err() → E
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L73"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or`

```python
unwrap_or(default: 'T') → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L76"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or_else`

```python
unwrap_or_else(op: 'Callable[[E], T]') → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L109"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or_raise`

```python
unwrap_or_raise(exception_type: 'type[BaseException]') → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L70"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `value_or`

```python
value_or(default: 'T') → T
```






---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L119"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `UnwrapError`
Exception raised when an unwrap or expect operation fails on a Result. 

```
try:
     Err("fail").unwrap()
except UnwrapError as e:
     print(e)
# Called `Result.unwrap()` on an `Err` value: 'fail'
``` 

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L134"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L161"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Ok`
Represents a successful result containing a value. 

Use when operations succeed and you want to chain further operations. Avoid when you need to represent failure states - use Err instead. 

```
Ok(42).unwrap()  # 42
``` 

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L176"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(value: 'T') → None
```






---

#### <kbd>property</kbd> ok_value







---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L213"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `alt`

```python
alt(op: 'Callable[[E], F]') → Ok[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L252"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `and_then`

```python
and_then(op: 'Callable[[T], Result[U, E]]') → Result[U, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L255"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `and_then_async`

```python
and_then_async(op: 'Callable[[T], Awaitable[Result[U, E]]]') → Result[U, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L203"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `err`

```python
err() → None
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L216"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expect`

```python
expect(message: 'str') → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L219"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expect_err`

```python
expect_err(message: 'str') → NoReturn
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L261"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `inspect`

```python
inspect(op: 'Callable[[T], Any]') → Ok[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L265"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `inspect_err`

```python
inspect_err(op: 'Callable[[E], Any]') → Ok[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L197"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_err`

```python
is_err() → Literal[False]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L194"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_ok`

```python
is_ok() → Literal[True]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L237"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map`

```python
map(op: 'Callable[[T], U]') → Ok[U, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L240"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_async`

```python
map_async(op: 'Callable[[T], Awaitable[U]]') → Ok[U, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L249"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_err`

```python
map_err(op: 'Callable[[E], F]') → Ok[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L243"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_or`

```python
map_or(default: 'U', op: 'Callable[[T], U]') → U
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L246"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_or_else`

```python
map_or_else(default_op: 'Callable[[], U]', op: 'Callable[[T], U]') → U
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L268"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `match`

```python
match(
    ok: 'Callable[[T], U] | None' = None,
    err: 'Callable[[E], U] | None' = None
) → U
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L200"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ok`

```python
ok() → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L258"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `or_else`

```python
or_else(op: 'Callable[[E], Result[T, F]]') → Ok[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L222"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap`

```python
unwrap() → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L225"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_err`

```python
unwrap_err() → NoReturn
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L228"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or`

```python
unwrap_or(default: 'T') → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L231"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or_else`

```python
unwrap_or_else(op: 'Callable[[E], T]') → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L234"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or_raise`

```python
unwrap_or_raise(exception_type: 'type[BaseException]') → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L210"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `value_or`

```python
value_or(default: 'T') → T
```






---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L274"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Err`
Represents a failed result containing an error value. 

Use when operations fail and you want to propagate error information. Avoid when success is the only meaningful outcome. 

```
Err("fail").unwrap_or(0)  # 0
``` 

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L289"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(value: 'E') → None
```






---

#### <kbd>property</kbd> err_value





---

#### <kbd>property</kbd> trace







---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L341"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `alt`

```python
alt(op: 'Callable[[E], F]') → Result[T, F]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L386"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `and_then`

```python
and_then(op: 'Callable[[T], Result[U, E]]') → Err[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L389"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `and_then_async`

```python
and_then_async(op: 'Callable[[T], Awaitable[Result[U, E]]]') → Err[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L331"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `err`

```python
err() → E
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L344"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expect`

```python
expect(message: 'str') → NoReturn
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L350"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expect_err`

```python
expect_err(message: 'str') → E
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L395"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `inspect`

```python
inspect(op: 'Callable[[T], Any]') → Err[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L398"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `inspect_err`

```python
inspect_err(op: 'Callable[[E], Any]') → Err[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L325"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_err`

```python
is_err() → Literal[True]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L322"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_ok`

```python
is_ok() → Literal[False]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L371"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map`

```python
map(op: 'Callable[[T], U]') → Err[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L374"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_async`

```python
map_async(op: 'Callable[[T], Awaitable[U]]') → Err[T, E]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L383"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_err`

```python
map_err(op: 'Callable[[E], F]') → Err[T, F]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L377"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_or`

```python
map_or(default: 'U', op: 'Callable[[T], U]') → U
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L380"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_or_else`

```python
map_or_else(default_op: 'Callable[[], U]', op: 'Callable[[T], U]') → U
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L402"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `match`

```python
match(
    ok: 'Callable[[T], U] | None' = None,
    err: 'Callable[[E], U] | None' = None
) → U
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L328"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ok`

```python
ok() → None
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L392"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `or_else`

```python
or_else(op: 'Callable[[E], Result[T, F]]') → Result[T, F]
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L353"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap`

```python
unwrap() → NoReturn
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L359"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_err`

```python
unwrap_err() → E
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L362"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or`

```python
unwrap_or(default: 'T') → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L365"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or_else`

```python
unwrap_or_else(op: 'Callable[[E], T]') → T
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L368"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or_raise`

```python
unwrap_or_raise(exception_type: 'type[BaseException]') → NoReturn
```





---

<a href="https://github.com/simwai/rustico/tree/main/src\rustico\rustico.py#L338"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `value_or`

```python
value_or(default: 'T') → T
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
