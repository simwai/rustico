# rustico

[![PyPI - Version](https://img.shields.io/pypi/v/rustico.svg?color=purple)](https://pypi.org/project/rustico/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rustico.svg?color=purple)](https://pypi.org/project/rustico/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)

> **A Schrödinger's Cat for Python error handling: your result is both alive and dead—until you unwrap it.**

## What is `rustico`?

`rustico` brings the power and elegance of Rust's `Result` type to Python. Every operation is either a success (`Ok`) or a failure (`Err`), and you must explicitly handle both. No more try/except hell—just beautiful, predictable, and composable error handling.

## Schrödinger's Cat: The Metaphor

Imagine every function call as a box containing Schrödinger's cat. Until you open (unwrap) the box, the cat is both alive (`Ok`) and dead (`Err`). With `rustico`, you don't have to guess or hope—when you unwrap the result, you'll know exactly what you got, and you'll handle both cases explicitly.

## Key Features

- 🔒 **Can't Forget Error Handling**: The type system forces you to handle both cases
- 📍 **Precise Error Information**: Know exactly what and where things failed
- 🧩 **Composable**: Chain operations without nested try/except blocks
- 🎯 **Early Exit**: Stop processing on first error automatically
- 🔍 **Type Safe**: Your IDE knows about both success and error cases
- ⚡ **Async Support**: First-class support for async/await
- 🧪 **Test Friendly**: Easily mock and test error conditions

## Installation

Python 3.8+ is required.

You can install `rustico` using pip:

```bash
pip install rustico
```

## Quick Example

Here's a taste of how `rustico` simplifies error handling:

```python
from rustico import Ok, Err, Result

def divide(numerator: float, denominator: float) -> Result[float, str]:
    """Divides two numbers, returning an Ok result or an Err if division by zero occurs."""
    if denominator == 0:
        return Err("Cannot divide by zero!")
    return Ok(numerator / denominator)

# --- Usage Examples ---

# Successful division
result_success = divide(10, 2)
if result_success.is_ok():
    print(f"Success: {result_success.unwrap()}") # Output: Success: 5.0

# Failed division
result_failure = divide(10, 0)
if result_failure.is_err():
    print(f"Error: {result_failure.unwrap_err()}") # Output: Error: Cannot divide by zero!

# Chaining operations
def multiply_by_two(value: float) -> Result[float, str]:
    return Ok(value * 2)

chained_result = divide(20, 4).and_then(multiply_by_two)
if chained_result.is_ok():
    print(f"Chained Success: {chained_result.unwrap()}") # Output: Chained Success: 10.0

failed_chained_result = divide(20, 0).and_then(multiply_by_two)
if failed_chained_result.is_err():
    print(f"Chained Error: {failed_chained_result.unwrap_err()}") # Output: Chained Error: Cannot divide by zero!
```

For detailed documentation, see the [full documentation](docs/index.md).

## License

`rustico` is distributed under the MIT License. See the [LICENSE](LICENSE) file for more information.
