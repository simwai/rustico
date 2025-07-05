# Comparison with Other Libraries

This page compares `rustico` with other similar libraries in the Python ecosystem.

## Feature Comparison

| Library         | Ok/Err | do-notation | Async | Decorators | Type Guards | Tracebacks | Type Hints | Monads | Rust-like | Philosophy      | Size  |
|-----------------|--------|-------------|-------|------------|-------------|------------|------------|--------|-----------|-----------------|-------|
| **rustico**     | ✅     | ✅          | ✅    | ✅         | ✅          | ✅         | ✅         | ✅     | ✅        | CUPID, explicit | Small |
| result          | ✅     | ❌          | ❌    | ❌         | ❌          | ❌         | ✅         | Partial| ✅        | Simplicity      | Tiny  |
| returns         | ✅     | Partial     | ✅    | ✅         | ✅          | ❌         | ✅         | ✅     | Partial   | Functional      | Large |
| poltergeist     | ✅     | ❌          | ❌    | ❌         | ❌          | ❌         | ✅         | ❌     | ✅        | Minimalism      | Tiny  |
| rusty-errors    | ✅     | ❌          | ❌    | ❌         | ❌          | ❌         | ✅         | Partial| ✅        | Rust-inspired   | Small |

**Legend:**

- **do-notation:** Generator-based early-exit chaining
- **Async:** Native async/await support
- **Decorators:** Built-in function wrapping decorators
- **Type Guards:** `is_ok`, `is_err` for static analysis
- **Tracebacks:** Captures exception tracebacks in `Err`
- **Monads:** Supports chaining, mapping, flatMap operations
- **Rust-like:** API and philosophy inspired by Rust

## Detailed Comparison

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

## Code Comparison

### Basic Usage

#### rustico

```python
from rustico import Ok, Err, as_result

@as_result(ValueError)
def parse_int(s: str) -> int:
    return int(s)

result = parse_int("123")
if result.is_ok():
    print(result.unwrap())  # 123
else:
    print(f"Error: {result.unwrap_err()}")
```

#### result

```python
from result import Ok, Err, Result

def parse_int(s: str) -> Result[int, ValueError]:
    try:
        return Ok(int(s))
    except ValueError as e:
        return Err(e)

result = parse_int("123")
if result.is_ok():
    print(result.unwrap())  # 123
else:
    print(f"Error: {result.unwrap_err()}")
```

#### returns

```python
from returns.result import Success, Failure, Result
from returns.functions import raise_exception

def parse_int(s: str) -> Result[int, ValueError]:
    try:
        return Success(int(s))
    except ValueError as e:
        return Failure(e)

result = parse_int("123")
result.map(print)  # 123
result.alt(raise_exception)
```

### Chaining Operations

#### rustico

```python
from rustico import Ok, Err, do

@do
def process():
    x = yield parse_int("10")
    y = yield parse_int("20")
    return x + y

result = process()
print(result)  # Ok(30)
```

#### result

```python
from result import Ok, Err

def process():
    x_result = parse_int("10")
    if x_result.is_err():
        return x_result
    
    y_result = parse_int("20")
    if y_result.is_err():
        return y_result
    
    return Ok(x_result.unwrap() + y_result.unwrap())

result = process()
print(result)  # Ok(30)
```

#### returns

```python
from returns.result import Success, Failure
from returns.functions import raise_exception

def process():
    return parse_int("10").bind(
        lambda x: parse_int("20").map(
            lambda y: x + y
        )
    )

result = process()
print(result)  # Success(30)
```

## Why Choose rustico?

- **Balanced Approach:** Not too minimal, not too complex
- **Async-First:** Built with modern async Python in mind
- **Developer Experience:** Excellent type hints and IDE integration
- **Explicit Error Handling:** Makes error cases impossible to ignore
- **Traceback Capture:** Preserves stack traces for better debugging
- **Pattern Matching:** First-class support for Python 3.10+ pattern matching
- **Composable:** Easy to chain operations with do-notation
- **Rust-Inspired:** Familiar API for Rust developers

Choose `rustico` if you want a modern, well-balanced Result type implementation that works well with both synchronous and asynchronous code, provides excellent developer experience, and makes error handling explicit and composable.
