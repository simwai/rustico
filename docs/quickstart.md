# Quick Start

This guide will help you get started with `rustico` quickly. We'll cover the basics of using the `Result` type and show you how it compares to traditional error handling.

## The Problem with Traditional Error Handling

Traditional error handling in Python using try/except blocks can be verbose, error-prone, and difficult to compose:

```python
def process_user_data(user_id: str, age_str: str):
    try:
        user_id_int = int(user_id)
    except ValueError:
        return None  # Lost error information!
    
    try:
        age = int(age_str)
    except ValueError:
        return None  # Which field failed?
    
    try:
        if age < 0:
            raise ValueError("Age cannot be negative")
        return {"user_id": user_id_int, "age": age}
    except ValueError:
        return None  # Nested try/except hell!

# Usage - You have to remember to check for None!
result = process_user_data("123", "25")
if result is None:  # But WHY did it fail?
    print("Something went wrong...")
```

## The `rustico` Way

With `rustico`, error handling becomes explicit, composable, and clear:

```python
from rustico import as_result, do, Ok, Err

@as_result(ValueError)
def parse_int(s: str) -> int:
    return int(s)

@do
def process_user_data(user_id: str, age_str: str):
    # Each step is explicit and composable
    user_id_int = yield parse_int(user_id)
    age = yield parse_int(age_str)
    
    if age < 0:
        return Err("Age cannot be negative")
    
    return {"user_id": user_id_int, "age": age}

# Usage - Errors are explicit and informative
result = process_user_data("123", "25")
match result:
    case Ok(data):
        print(f"Success: {data}")
    case Err(error):
        print(f"Failed because: {error}")
```

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

## Composing Multiple Steps (do-notation)

```python
from rustico import as_result, do

@do
def example():
    # This yields Result[int, ValueError]
    x = yield Ok(10)  # x receives the unwrapped int (type T)
    y = yield Ok(20)  # y receives the unwrapped int (type T)
    return x + y     

print(example())  # Ok(30)
```

## Early Exit on Error

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

## Async Example

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

asyncio.run(main())  # Async sum: 123
```

## Mapping and Error Transformation

```python
result = parse_int("not a number").map(lambda x: x * 2).map_err(str)
print(result)  # Err('invalid literal for int() with base 10: ...')
```

For more detailed examples and advanced usage, check out the [Examples](examples.md) section.
