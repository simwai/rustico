# rustico

> **A Schrödinger's Cat for Python error handling: your result is both alive and dead—until you unwrap it.**

## What is `rustico`?

`rustico` brings the power and elegance of Rust's `Result` type to Python. Every operation is either a success (`Ok`) or a failure (`Err`), and you must explicitly handle both. No more try/except hell—just beautiful, predictable, and composable error handling.

---

## Schrödinger's Cat: The Metaphor

Imagine every function call as a box containing Schrödinger's cat. Until you open (unwrap) the box, the cat is both alive (`Ok`) and dead (`Err`). With `rustico`, you don't have to guess or hope—when you unwrap the result, you'll know exactly what you got, and you'll handle both cases explicitly.

---

## Why `rustico`? (CUPID Principle)

- **Composability:** Chain operations with `.map`, `.and_then`, and more.
- **Unix philosophy:** Functions do one thing, return one result.
- **Predictability:** No hidden exceptions. Every error is explicit.
- **Idiomatic:** Inspired by Rust, but designed for Python.
- **Declarative:** Your code describes what happens, not how to handle chaos.

---

## 🚀 Quick Start: The Most Recommended Form

Replace this:

```python
def parse_int(s: str) -> int:
    return int(s)
```

With this, using `@as_result`:

```python
from rustico import as_result

@as_result(ValueError)
def parse_int(s: str) -> int:
    return int(s)

result = parse_int("42")
if result.is_ok():
    print("Parsed:", result.unwrap())
else:
    print("Error:", result.unwrap_err())
```

---

## Comparison with Other Libraries

| Library         | Ok/Err | do-notation | Async | Decorators | Type Guards | Tracebacks | Type Hints | Monads | Rust-like | Philosophy      | Size  |
|-----------------|--------|-------------|-------|------------|-------------|------------|------------|--------|-----------|-----------------|-------|
| **rustico**     | ✅     | ✅          | ✅    | ✅         | ✅          | ✅         | ✅         | ✅     | ✅        | CUPID, explicit | Small |
| result          | ✅     | ❌          | ❌    | ❌         | ❌          | ❌         | ✅         | Partial| ✅        | Simplicity      | Tiny  |
| returns         | ✅     | Partial     | ✅    | ✅         | ✅          | ❌         | ✅         | ✅     | Partial   | Functional      | Large |
| poltergeist     | ✅     | ❌          | ❌    | ❌         | ❌          | ❌         | ✅         | ❌     | ✅        | Minimalism      | Tiny  |
| rusty-errors    | ✅     | ❌          | ❌    | ❌         | ❌          | ❌         | ✅         | Partial| ✅        | Rust-inspired   | Small |

**Detailed Comparison:**

### **rustico** (This Library)

- **Strengths:** Full-featured, async-first, excellent TypeScript-like developer experience
- **Philosophy:** CUPID principle - Composable, Unix-like, Predictable, Idiomatic, Declarative
- **Best for:** New projects, async workflows, teams wanting explicit error handling
- **Unique features:** Traceback capture, do-notation, dual-mode decorators

### **result**

- **Strengths:** Simple, lightweight, battle-tested
- **Philosophy:** Keep it simple and close to Rust's API
- **Best for:** Simple sync applications, minimal dependencies
- **Limitations:** No async support, no decorators, basic feature set

### **returns**

- **Strengths:** Rich functional programming features, extensive ecosystem
- **Philosophy:** Bring functional programming concepts to Python
- **Best for:** FP enthusiasts, complex data transformation pipelines
- **Unique features:** Maybe, IO, containers, railway-oriented programming
- **Limitations:** Learning curve, heavy dependency

### **poltergeist**

- **Strengths:** Extremely minimal, zero dependencies
- **Philosophy:** Minimalism above all
- **Best for:** Embedded systems, minimal footprint requirements
- **Limitations:** Very basic feature set, no advanced operations

### **rusty-errors**

- **Strengths:** Close to Rust's Result API
- **Philosophy:** Direct Rust port
- **Best for:** Rust developers transitioning to Python
- **Limitations:** Limited Python-specific features, no async

**Legend:**

- **do-notation:** Generator-based early-exit chaining
- **Async:** Native async/await support
- **Decorators:** Built-in function wrapping decorators
- **Type Guards:** `is_ok`, `is_err` for static analysis
- **Tracebacks:** Captures exception tracebacks in `Err`
- **Monads:** Supports chaining, mapping, flatMap operations
- **Rust-like:** API and philosophy inspired by Rust

---

## Basic Usage Examples

### 1. Wrapping Functions

```python
from rustico import as_result

@as_result(ValueError)
def parse_int(s: str) -> int:
    return int(s)

print(parse_int("123"))    # Ok(123)
print(parse_int("oops"))   # Err(ValueError(...))
```

### 2. Handling Results

```python
result = parse_int("456")
if result.is_ok():
    value = result.unwrap()
    print("Got:", value)
else:
    error = result.unwrap_err()
    print("Failed:", error)
```

### 3. Chaining Operations

```python
from rustico import Ok, Err

def double(x: int):
    return Ok(x * 2)

result = parse_int("21").and_then(double)
print(result)  # Ok(42)
```

---

## Realistic & More Complex Scenarios

### 1. Composing Multiple Steps (do-notation)

```python
from rustico import as_result, do

@as_result(ValueError)
def parse_int(s: str) -> int:
    return int(s)

@do
def compute():
    a = yield parse_int("10")
    b = yield parse_int("20")
    return a + b

result = compute()
if result.is_ok():
    print("Sum:", result.unwrap())
else:
    print("Error:", result.unwrap_err())
```

### 2. Early Exit on Error

```python
@do
def safe_division(a: str, b: str):
    x = yield parse_int(a)
    y = yield parse_int(b)
    if y == 0:
        return Err("Division by zero")
    return x / y

print(safe_division("100", "0"))   # Err('Division by zero')
print(safe_division("100", "5"))   # Ok(20.0)
print(safe_division("foo", "5"))   # Err(ValueError(...))
```

### 3. Async Example

```python
import asyncio
from rustico import as_async_result, do_async

@as_async_result(ValueError)
async def parse_int_async(s: str) -> int:
    await asyncio.sleep(0.1)
    return int(s)

@do_async
async def compute_async():
    a = yield await parse_int_async("100")
    b = yield await parse_int_async("23")
    return a + b

async def main():
    result = await compute_async()
    if result.is_ok():
        print("Async sum:", result.unwrap())
    else:
        print("Async error:", result.unwrap_err())

asyncio.run(main())
```

### 4. Mapping and Error Transformation

```python
result = parse_int("not a number").map(lambda x: x * 2).map_err(str)
print(result)  # Err('invalid literal for int() with base 10: ...')
```

---

## API Reference

### Types

#### `Ok(value: T)`

Represents a successful result containing a value.

---

**Basic Inspection**

- **ok() -> T**  
  *Returns the inner value.*  

  ```python
  result = Ok(42)
  print(result.ok())  # 42
  ```

- **err() -> None**  
  *Always returns `None` for `Ok` values.*  

  ```python
  result = Ok(42)
  print(result.err())  # None
  ```

- **is_ok() -> True**  
  *Type-safe way to check if result is successful.*  

  ```python
  result = Ok(42)
  if result.is_ok():
      print("Success!")
  ```

- **is_err() -> False**  
  *Type-safe way to check if result is an error.*  

  ```python
  result = Ok(42)
  if not result.is_err():
      print("Not an error")
  ```

---

**Extracting Values**

- **unwrap() -> T**  
  *Extracts the value or raises `UnwrapError` if called on `Err`.*  

  ```python
  result = Ok(42)
  value = result.unwrap()  # 42
  
  # Use when you're certain it's Ok
  config = load_config().unwrap()
  ```

- **unwrap_err() -> NoReturn**  
  *Always raises `UnwrapError` for `Ok` values.*  

  ```python
  result = Ok(42)
  # result.unwrap_err()  # UnwrapError!
  ```

- **unwrap_or(default: U) -> T**  
  *Returns the value, or the default if `Err`.*  

  ```python
  result = Ok(42)
  value = result.unwrap_or(0)  # 42
  
  # Useful for providing fallbacks
  port = get_port_from_env().unwrap_or(8080)
  ```

- **unwrap_or_else(fn: Callable[[E], T]) -> T**  
  *Returns the value, or calls `fn` with the error if `Err`.*  

  ```python
  result = Ok(42)
  value = result.unwrap_or_else(lambda e: 0)  # 42
  
  # Useful for computed defaults
  timeout = get_timeout().unwrap_or_else(lambda _: calculate_default_timeout())
  ```

- **unwrap_or_raise(exc_type: type[BaseException]) -> T**  
  *Returns the value, or raises the specified exception if `Err`.*  

  ```python
  result = Ok(42)
  value = result.unwrap_or_raise(ValueError)  # 42
  
  # Convert Result to exception-based flow
  user_id = authenticate().unwrap_or_raise(AuthenticationError)
  ```

---

**Transforming Values**

- **map(fn: Callable[[T], U]) -> Ok[U]**  
  *Transforms the value using the provided function.*  

  ```python
  result = Ok(21)
  doubled = result.map(lambda x: x * 2)  # Ok(42)
  
  # Chain transformations
  user = get_user().map(lambda u: u.upper()).map(lambda u: u.strip())
  ```

- **map_async(fn: Callable[[T], Awaitable[U]]) -> Awaitable[Ok[U]]**  
  *Async version of `map`.*  

  ```python
  result = Ok("user123")
  user_data = await result.map_async(fetch_user_data)  # Ok(UserData(...))
  ```

- **map_or(default: U, fn: Callable[[T], U]) -> U**  
  *Maps the value or returns default if `Err`.*  

  ```python
  result = Ok(5)
  length = result.map_or(0, len)  # Doesn't apply here, but shows pattern
  
  # Better example with strings
  name = get_name().map_or("Anonymous", lambda n: n.title())
  ```

- **map_or_else(default_fn: Callable[[], U], fn: Callable[[T], U]) -> U**  
  *Maps the value or calls default function if `Err`.*  

  ```python
  result = Ok("hello")
  length = result.map_or_else(lambda: 0, len)  # 5
  
  # Useful for expensive default computations
  data = fetch_data().map_or_else(generate_default_data, process_data)
  ```

- **map_err(fn: Callable[[E], F]) -> Ok[T]**  
  *No-op for `Ok` values; transforms error type for `Err`.*  

  ```python
  result = Ok(42)
  same_result = result.map_err(str)  # Ok(42) - unchanged
  
  # Useful in pipelines where you want to standardize error types
  result = fetch_data().map_err(lambda e: f"Network error: {e}")
  ```

---

**Chaining Operations**

- **and_then(fn: Callable[[T], Result[U, E]]) -> Result[U, E]**  
  *Chains operations that may fail. Also called "flatMap" or "bind".*  

  ```python
  def parse_int(s: str) -> Result[int, str]:
      try:
          return Ok(int(s))
      except ValueError:
          return Err("Invalid number")
  
  def divide_by_two(x: int) -> Result[float, str]:
      return Ok(x / 2.0)
  
  result = Ok("42").and_then(parse_int).and_then(divide_by_two)  # Ok(21.0)
  
  # Database operations
  user = get_user_id().and_then(fetch_user).and_then(validate_user)
  ```

- **and_then_async(fn: Callable[[T], Awaitable[Result[U, E]]]) -> Awaitable[Result[U, E]]**  
  *Async version of `and_then`.*  

  ```python
  result = Ok("user123")
  user_data = await result.and_then_async(async_fetch_user)
  ```

- **or_else(fn: Callable[[E], Result[T, F]]) -> Ok[T]**  
  *No-op for `Ok` values; handles error case for `Err`.*  

  ```python
  result = Ok(42)
  same_result = result.or_else(lambda e: Ok(0))  # Ok(42) - unchanged
  
  # Useful for error recovery
  data = fetch_primary_data().or_else(lambda _: fetch_backup_data())
  ```

---

**Utilities**

- **swap() -> Err[T]**  
  *Swaps `Ok` and `Err` cases.*  

  ```python
  result = Ok(42)
  swapped = result.swap()  # Err(42)
  
  # Useful for inverting logic
  not_found = find_item().swap()  # Now Ok means "not found"
  ```

- **value_or(default: Any) -> T**  
  *Alias for `unwrap_or`. Returns value or default.*  

  ```python
  result = Ok(42)
  value = result.value_or(0)  # 42
  
  # More readable in some contexts
  max_connections = get_max_connections().value_or(100)
  ```

- **alt(fn: Callable[[E], F]) -> Ok[T]**  
  *No-op for `Ok` values; transforms error for `Err`.*  

  ```python
  result = Ok(42)
  same_result = result.alt(lambda e: f"Error: {e}")  # Ok(42) - unchanged
  ```

- **expect(msg: str) -> T**  
  *Like `unwrap()` but with a custom error message.*  

  ```python
  result = Ok(42)
  value = result.expect("Should have a value")  # 42
  
  # Better error messages for debugging
  config = load_config().expect("Config file should be valid")
  ```

- **expect_err(msg: str) -> NoReturn**  
  *Always raises `UnwrapError` with custom message for `Ok` values.*  

  ```python
  result = Ok(42)
  # result.expect_err("Expected error")  # UnwrapError!
  ```

---

**Debugging & Side Effects**

- **inspect(fn: Callable[[T], Any]) -> Ok[T]**  
  *Calls function with the value for side effects, returns original result.*  

  ```python
  result = Ok(42)
  same_result = result.inspect(lambda x: print(f"Value: {x}"))  # Prints: Value: 42
  
  # Useful for debugging pipelines
  result = fetch_data().inspect(lambda data: logger.info(f"Fetched {len(data)} items"))
  ```

- **inspect_err(fn: Callable[[E], Any]) -> Ok[T]**  
  *No-op for `Ok` values; logs error for `Err`.*  

  ```python
  result = Ok(42)
  same_result = result.inspect_err(lambda e: print(f"Error: {e}"))  # No output
  
  # Useful for logging errors without handling them
  result = fetch_data().inspect_err(lambda e: logger.error(f"Fetch failed: {e}"))
  ```

---

#### `Err(error: E)`

Represents a failed result containing an error.

---

**Basic Inspection**

- **ok() -> None**  
  *Always returns `None` for `Err` values.*  

  ```python
  result = Err("Something went wrong")
  print(result.ok())  # None
  ```

- **err() -> E**  
  *Returns the error value.*  

  ```python
  result = Err("Something went wrong")
  print(result.err())  # "Something went wrong"
  ```

- **is_ok() -> False**  
  *Type-safe way to check if result is successful.*  

  ```python
  result = Err("error")
  if not result.is_ok():
      print("This is an error")
  ```

- **is_err() -> True**  
  *Type-safe way to check if result is an error.*  

  ```python
  result = Err("error")
  if result.is_err():
      print("Handle the error")
  ```

---

**Extracting Values**

- **unwrap() -> NoReturn**  
  *Always raises `UnwrapError` for `Err` values.*  

  ```python
  result = Err("Something went wrong")
  # value = result.unwrap()  # UnwrapError!
  
  # Only use when you're certain it's Ok
  # Better to check first:
  if result.is_ok():
      value = result.unwrap()
  ```

- **unwrap_err() -> E**  
  *Extracts the error value.*  

  ```python
  result = Err("Connection failed")
  error = result.unwrap_err()  # "Connection failed"
  
  # Useful when you want to handle the specific error
  if result.is_err():
      error_msg = result.unwrap_err()
      logger.error(f"Operation failed: {error_msg}")
  ```

- **unwrap_or(default: U) -> U**  
  *Returns the default value since this is an error.*  

  ```python
  result = Err("Connection failed")
  value = result.unwrap_or(42)  # 42
  
  # Provide fallback values
  port = get_port_from_config().unwrap_or(8080)
  timeout = get_timeout().unwrap_or(30.0)
  ```

- **unwrap_or_else(fn: Callable[[E], T]) -> T**  
  *Calls function with the error to compute a fallback value.*  

  ```python
  result = Err("Invalid input")
  value = result.unwrap_or_else(lambda e: len(e))  # 13
  
  # Compute fallback based on error
  data = fetch_data().unwrap_or_else(lambda _: generate_empty_dataset())
  retry_count = operation().unwrap_or_else(lambda e: calculate_retry_count(e))
  ```

- **unwrap_or_raise(exc_type: type[BaseException]) -> NoReturn**  
  *Raises the specified exception with the error value.*  

  ```python
  result = Err("Invalid credentials")
  # result.unwrap_or_raise(ValueError)  # ValueError("Invalid credentials")
  
  # Convert Result errors to specific exceptions
  user = authenticate().unwrap_or_raise(AuthenticationError)
  data = validate_input().unwrap_or_raise(ValidationError)
  ```

---

**Transforming Values**

- **map(fn: Callable[[T], U]) -> Err[E]**  
  *No-op for `Err` values; preserves the error.*  

  ```python
  result = Err("Parse error")
  same_result = result.map(lambda x: x * 2)  # Err("Parse error") - unchanged
  
  # Useful in pipelines where errors propagate
  result = parse_data().map(validate_data).map(process_data)
  # If parse_data fails, subsequent maps are skipped
  ```

- **map_async(fn: Callable[[T], Awaitable[U]]) -> Awaitable[Err[E]]**  
  *Async no-op for `Err` values.*  

  ```python
  result = Err("Network error")
  same_result = await result.map_async(async_transform)  # Err("Network error")
  ```

- **map_or(default: U, fn: Callable[[T], U]) -> U**  
  *Returns the default value since this is an error.*  

  ```python
  result = Err("Parse error")
  length = result.map_or(0, len)  # 0
  
  # Provide default transformations
  name_length = get_name().map_or(0, len)
  formatted_date = parse_date().map_or("Unknown", lambda d: d.strftime("%Y-%m-%d"))
  ```

- **map_or_else(default_fn: Callable[[], U], fn: Callable[[T], U]) -> U**  
  *Calls the default function since this is an error.*  

  ```python
  result = Err("Database error")
  value = result.map_or_else(lambda: "No data", lambda x: x.upper())  # "No data"
  
  # Compute expensive defaults only when needed
  data = fetch_data().map_or_else(generate_default_data, process_data)
  ```

- **map_err(fn: Callable[[E], F]) -> Err[F]**  
  *Transforms the error value using the provided function.*  

  ```python
  result = Err(ValueError("Invalid number"))
  string_error = result.map_err(str)  # Err("Invalid number")
  
  # Standardize error types
  result = parse_json().map_err(lambda e: f"JSON Error: {e}")
  api_result = call_api().map_err(lambda e: ApiError(str(e)))
  ```

---

**Chaining Operations**

- **and_then(fn: Callable[[T], Result[U, E]]) -> Err[E]**  
  *No-op for `Err` values; preserves the error.*  

  ```python
  result = Err("Parse error")
  same_result = result.and_then(lambda x: Ok(x * 2))  # Err("Parse error")
  
  # Errors short-circuit the chain
  result = parse_input().and_then(validate_input).and_then(process_input)
  # If parse_input fails, validation and processing are skipped
  ```

- **and_then_async(fn: Callable[[T], Awaitable[Result[U, E]]]) -> Awaitable[Err[E]]**  
  *Async no-op for `Err` values.*  

  ```python
  result = Err("Network error")
  same_result = await result.and_then_async(async_process)  # Err("Network error")
  ```

- **or_else(fn: Callable[[E], Result[T, F]]) -> Result[T, F]**  
  *Handles the error case by calling the provided function.*  

  ```python
  result = Err("Primary server down")
  backup_result = result.or_else(lambda e: try_backup_server())
  
  # Error recovery patterns
  data = fetch_from_cache().or_else(lambda _: fetch_from_database())
  config = load_user_config().or_else(lambda _: load_default_config())
  ```

---

**Utilities**

- **swap() -> Ok[E]**  
  *Swaps `Ok` and `Err` cases, turning error into success.*  

  ```python
  result = Err("Not found")
  swapped = result.swap()  # Ok("Not found")
  
  # Useful for inverting logic
  not_exists = file_exists().swap()  # Ok means "file doesn't exist"
  ```

- **value_or(default: U) -> U**  
  *Alias for `unwrap_or`. Returns default since this is an error.*  

  ```python
  result = Err("Connection failed")
  value = result.value_or(42)  # 42
  
  # Readable default handling
  max_retries = get_max_retries().value_or(3)
  ```

- **alt(fn: Callable[[E], F]) -> Err[F]**  
  *Transforms the error value using the provided function.*  

  ```python
  result = Err("timeout")
  enhanced_error = result.alt(lambda e: f"Network {e}")  # Err("Network timeout")
  
  # Add context to errors
  result = fetch_data().alt(lambda e: f"Failed to fetch user data: {e}")
  ```

- **expect(msg: str) -> NoReturn**  
  *Always raises `UnwrapError` with custom message for `Err` values.*  

  ```python
  result = Err("Connection failed")
  # value = result.expect("Should have connected")  # UnwrapError: Should have connected: 'Connection failed'
  
  # Better error messages for debugging
  # config = load_config().expect("Config file should be valid")
  ```

- **expect_err(msg: str) -> E**  
  *Returns the error value (like `unwrap_err` but with custom message context).*  

  ```python
  result = Err("Connection failed")
  error = result.expect_err("Expected this to fail")  # "Connection failed"
  
  # Document expected error cases
  validation_error = validate_input().expect_err("Validation should catch this")
  ```

---

**Debugging & Side Effects**

- **inspect(fn: Callable[[T], Any]) -> Err[E]**  
  *No-op for `Err` values; doesn't call the function.*  

  ```python
  result = Err("Parse error")
  same_result = result.inspect(lambda x: print(f"Value: {x}"))  # No output
  
  # Success-only side effects
  result = fetch_data().inspect(lambda data: logger.info(f"Fetched {len(data)} items"))
  ```

- **inspect_err(fn: Callable[[E], Any]) -> Err[E]**  
  *Calls function with the error for side effects, returns original result.*  

  ```python
  result = Err("Connection timeout")
  same_result = result.inspect_err(lambda e: print(f"Error: {e}"))  # Prints: Error: Connection timeout
  
  # Useful for logging errors without handling them
  result = fetch_data().inspect_err(lambda e: logger.error(f"Fetch failed: {e}"))
  metrics = call_api().inspect_err(lambda e: increment_error_counter(type(e)))
  ```

- **trace: Optional[List[str]]**  
  *Contains the formatted traceback if the error is a Python exception.*  

  ```python
  try:
      raise ValueError("Something went wrong")
  except ValueError as e:
      result = Err(e)
      if result.trace:
          print("Traceback:")
          for line in result.trace:
              print(line)
  ```

---

### Decorators

#### `@as_result(*exceptions)`

*Converts a function to return `Result` instead of raising exceptions.*

```python
@as_result(ValueError, TypeError)
def parse_and_double(s: str) -> int:
    return int(s) * 2

result = parse_and_double("21")  # Ok(42)
result = parse_and_double("foo")  # Err(ValueError(...))

# Multiple exception types
@as_result(FileNotFoundError, PermissionError, IOError)
def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()

content = read_file("config.txt")
if content.is_ok():
    print(content.unwrap())
else:
    print(f"Failed to read file: {content.unwrap_err()}")
```

#### `@as_async_result(*exceptions)`

*Async version of `as_result`.*

```python
@as_async_result(aiohttp.ClientError, asyncio.TimeoutError)
async def fetch_url(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

result = await fetch_url("https://api.example.com")
if result.is_ok():
    data = result.unwrap()
else:
    print(f"Request failed: {result.unwrap_err()}")
```

#### `@catch(*exceptions)`

*Simplified version of `as_result` for quick wrapping.*

```python
@catch(ZeroDivisionError)
def divide(a: int, b: int) -> float:
    return a / b

result = divide(10, 2)  # Ok(5.0)
result = divide(10, 0)  # Err(ZeroDivisionError(...))
```

#### `@catch_async(*exceptions)`

*Async version of `catch`.*

```python
@catch_async(ConnectionError)
async def ping_server(host: str) -> bool:
    # ... async ping logic
    return True

result = await ping_server("example.com")
```

---

### Do-notation

#### `@do`

*Enables early-exit syntax using generators. Automatically unwraps `Ok` values and exits on `Err`.*

```python
@do
def complex_operation(a: str, b: str, c: str):
    # Each yield unwraps an Ok or exits with Err
    x = yield parse_int(a)
    y = yield parse_int(b)
    z = yield parse_int(c)
    
    # Regular Python logic
    if x + y > z:
        return "Sum is greater"
    else:
        return "Sum is not greater"

result = complex_operation("10", "20", "15")  # Ok("Sum is greater")
result = complex_operation("10", "foo", "15")  # Err(ValueError(...))

# Database operations
@do
def create_user_with_profile(email: str, name: str):
    user = yield create_user(email)
    profile = yield create_profile(user.id, name)
    yield send_welcome_email(user.email)
    return UserWithProfile(user, profile)
```

#### `@do_async`

*Async version of do-notation.*

```python
@do_async
async def fetch_user_data(user_id: int):
    user = yield await fetch_user(user_id)
    profile = yield await fetch_profile(user.id)
    posts = yield await fetch_posts(user.id)
    return UserData(user, profile, posts)

# Usage
result = await fetch_user_data(123)
if result.is_ok():
    user_data = result.unwrap()
    print(f"User: {user_data.user.name}")
```

---

### Utilities

#### `is_ok(result: Result[T, E]) -> bool`

*Type guard that helps with static analysis and type narrowing.*

```python
result = parse_int("42")
if is_ok(result):
    # Type checker knows this is Ok[int]
    value = result.unwrap()  # Safe!
    print(f"Parsed: {value}")
```

#### `is_err(result: Result[T, E]) -> bool`

*Type guard for error cases.*

```python
result = parse_int("foo")
if is_err(result):
    # Type checker knows this is Err[ValueError]
    error = result.unwrap_err()  # Safe!
    print(f"Error: {error}")
```

---

### Exceptions

#### `UnwrapError`

*Raised when attempting to unwrap the wrong variant.*

```python
try:
    result = Err("Something went wrong")
    value = result.unwrap()  # This will raise UnwrapError
except UnwrapError as e:
    print(f"Unwrap failed: {e}")
    original_result = e.result  # Access the original Result
    if original_result.is_err():
        print(f"Original error: {original_result.unwrap_err()}")
```

---

## Advanced Usage Patterns

### Error Recovery Chains

```python
@do
def robust_data_fetch(user_id: int):
    # Try multiple data sources with fallbacks
    data = yield (
        fetch_from_cache(user_id)
        .or_else(lambda _: fetch_from_database(user_id))
        .or_else(lambda _: fetch_from_backup(user_id))
        .or_else(lambda _: Ok(get_default_user_data()))
    )
    
    # Validate and process
    validated = yield validate_user_data(data)
    processed = yield process_user_data(validated)
    
    return processed
```

### Conditional Error Handling

```python
def smart_retry(operation, max_retries=3):
    @do
    def attempt():
        for attempt in range(max_retries):
            result = yield operation()
            if result.is_ok():
                return result.unwrap()
            
            # Only retry on specific errors
            error = result.unwrap_err()
            if not isinstance(error, (ConnectionError, TimeoutError)):
                return result  # Don't retry on other errors
                
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                
        return result  # Final attempt failed
    
    return attempt()
```

### Parallel Operations with Results

```python
async def fetch_user_dashboard(user_id: int):
    # Launch multiple async operations
    user_task = asyncio.create_task(fetch_user(user_id))
    posts_task = asyncio.create_task(fetch_posts(user_id))
    notifications_task = asyncio.create_task(fetch_notifications(user_id))
    
    # Wait for all results
    user_result = await user_task
    posts_result = await posts_task  
    notifications_result = await notifications_task
    
    # Combine results - any error fails the whole operation
    @do
    def combine_results():
        user = yield user_result
        posts = yield posts_result
        notifications = yield notifications_result
        
        return DashboardData(user, posts, notifications)
    
    return combine_results()
```

### Type-Safe Error Handling

```python
from typing import Literal

def parse_config(content: str) -> Result[dict, Literal["json_error", "validation_error"]]:
    # Parse JSON
    json_result = catch(json.JSONDecodeError)(json.loads)(content)
    if json_result.is_err():
        return Err("json_error")
    
    # Validate structure
    data = json_result.unwrap()
    if not isinstance(data, dict) or "version" not in data:
        return Err("validation_error")
    
    return Ok(data)

# Usage with exhaustive error handling
config_result = parse_config(file_content)
match config_result:
    case Ok(config):
        print(f"Config version: {config['version']}")
    case Err("json_error"):
        print("Invalid JSON format")
    case Err("validation_error"):
        print("Missing required fields")
```

---

## Performance Considerations

### Memory Usage

- `Ok` and `Err` have minimal overhead (`__slots__` optimization)
- Traceback capture only occurs for `BaseException` types
- Generator-based do-notation is memory-efficient

### Speed

- Method calls have minimal overhead
- Short-circuiting in chains avoids unnecessary work
- Type guards enable compiler optimizations

### Best Practices

```python
# ✅ Good: Chain operations to avoid intermediate checks
result = (
    parse_input(data)
    .and_then(validate_input)  
    .and_then(process_input)
    .map(format_output)
)

# ❌ Avoid: Multiple unwrap checks
parse_result = parse_input(data)
if parse_result.is_ok():
    validate_result = validate_input(parse_result.unwrap())
    if validate_result.is_ok():
        # ... nested mess
```

---

## Migration Guide

### From Exception-Based Code

**Before:**

```python
def process_user_data(user_id: str):
    try:
        uid = int(user_id)
        user = database.get_user(uid)
        if not user:
            raise ValueError("User not found")
        return user.name.upper()
    except ValueError as e:
        logger.error(f"Invalid user ID: {e}")
        return None
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        return None
```

**After:**

```python
@as_result(ValueError, DatabaseError)
def get_user_name(user_id: str) -> str:
    uid = int(user_id)  # May raise ValueError
    user = database.get_user(uid)  # May raise DatabaseError
    if not user:
        raise ValueError("User not found")
    return user.name.upper()

# Usage
result = get_user_name("123")
match result:
    case Ok(name):
        print(f"User name: {name}")
    case Err(ValueError() as e):
        logger.error(f"Invalid user ID: {e}")
    case Err(DatabaseError() as e):
        logger.error(f"Database error: {e}")
```

### From Other Result Libraries

**From `result` library:**

```python
# Before (result library)
from result import Ok, Err

def old_way():
    return Ok(42).map(lambda x: x * 2)

# After (rustico)
from rustico import Ok, Err, do

@do  # New: do-notation support
def new_way():
    value = yield Ok(42)
    return value * 2
```

---

## Installation

```bash
pip install rustico
```

**Requirements:**

- Python 3.8+

**Optional dependencies:**

```bash
# For development
pip install rustico
```

---

## Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**
3. **Add tests for new functionality**
4. **Ensure all tests pass**
5. **Submit a pull request**

### Development Setup

```bash
git clone https://github.com/simwai/rustico
cd rustico
pip install -e ".[dev]"
pytest
```

### Code Style

- Follow PEP 8
- Use type hints everywhere
- Add docstrings for public APIs
- Include usage examples in docstrings

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

*"In the quantum realm of error handling, rustico collapses the wave function of uncertainty into the binary certainty of `Ok` or `Err`."*
