# Examples

This page contains practical examples of using `rustico` in real-world scenarios.

!!! note "About these examples"
    These examples demonstrate real-world use cases for `rustico`. They're designed to be copy-paste friendly and show best practices for error handling.

!!! tip "Pro tip"
    Most examples use the `@do` decorator for composing operations. This is the recommended approach for complex workflows.

[Get Started with Examples](#web-api-client){ .md-button .md-button--primary }
[View on GitHub](https://github.com/simwai/rustico/blob/main/docs/examples.md){ .md-button }

## Web API Client

> :octicons-rocket-16: **Use Case:** Making HTTP requests with proper error handling

```python
import requests
from rustico import as_result, do, Ok, Err, Result

@as_result(requests.RequestException)
def fetch_user(user_id: int) -> dict:
    response = requests.get(f"https://api.example.com/users/{user_id}")
    response.raise_for_status()
    return response.json()

@as_result(KeyError, TypeError)
def extract_email(user_data: dict) -> str:
    return user_data["email"]

@do
def get_user_email(user_id: int) -> Result[str, Exception]:
    user_data = yield fetch_user(user_id)
    email = yield extract_email(user_data)
    return email.lower()

# Usage
result = get_user_email(123)
match result:
    case Ok(email):
        print(f"User email: {email}")
    case Err(error):
        if isinstance(error, requests.ConnectionError):
            print("Network error. Please check your connection.")
        elif isinstance(error, requests.HTTPError):
            print(f"API error: {error}")
        elif isinstance(error, KeyError):
            print("User data is missing email field")
        else:
            print(f"Unexpected error: {error}")
```

## Database Operations

> :material-database: **Use Case:** Safe database interactions with automatic connection handling

```python
import sqlite3
from typing import List
from rustico import as_result, do, Ok, Err, Result

@as_result(sqlite3.Error)
def connect_db(db_path: str) -> sqlite3.Connection:
    return sqlite3.connect(db_path)

@as_result(sqlite3.Error)
def execute_query(conn: sqlite3.Connection, query: str, params: tuple = ()) -> List[tuple]:
    cursor = conn.cursor()
    cursor.execute(query, params)
    return cursor.fetchall()

@do
def get_user_posts(db_path: str, user_id: int) -> Result[List[dict], Exception]:
    conn = yield connect_db(db_path)
    
    try:
        rows = yield execute_query(
            conn, 
            "SELECT id, title, content FROM posts WHERE user_id = ?", 
            (user_id,)
        )
        
        posts = [
            {"id": row[0], "title": row[1], "content": row[2]}
            for row in rows
        ]
        
        return posts
    finally:
        conn.close()

# Usage
result = get_user_posts("app.db", 42)
if result.is_ok():
    posts = result.unwrap()
    print(f"Found {len(posts)} posts")
    for post in posts:
        print(f"- {post['title']}")
else:
    print(f"Database error: {result.unwrap_err()}")
```

## File Operations

> :material-file-document: **Use Case:** Reading and parsing configuration files safely

```python
import json
from pathlib import Path
from rustico import as_result, do, Ok, Err, Result

@as_result(FileNotFoundError, PermissionError)
def read_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")

@as_result(json.JSONDecodeError)
def parse_json(content: str) -> dict:
    return json.loads(content)

@do
def load_config(config_path: str) -> Result[dict, Exception]:
    content = yield read_file(config_path)
    config = yield parse_json(content)
    
    # Validate config
    if "api_key" not in config:
        return Err(ValueError("Missing required 'api_key' in config"))
    
    return config

# Usage
result = load_config("config.json")
config = result.unwrap_or({
    "api_key": "default_key",
    "timeout": 30,
    "debug": False
})

print(f"Using API key: {config['api_key']}")
```

## Error Handling Patterns

!!! warning "Common Pitfalls"
    Remember that `unwrap()` will raise an exception if called on an `Err` result. Always check with `is_ok()` first or use `unwrap_or()` if you need a fallback value.

### Fallback Values

```python
from rustico import as_result, Ok, Err

@as_result(ValueError)
def parse_int(s: str) -> int:
    return int(s)

# Using unwrap_or for fallback
port = parse_int(os.environ.get("PORT", "")).unwrap_or(8080)
print(f"Starting server on port {port}")
```

### Transforming Errors

```python
from rustico import as_result, Ok, Err

@as_result(ValueError)
def parse_int(s: str) -> int:
    return int(s)

# Transform error to a user-friendly message
result = parse_int("abc").map_err(lambda e: f"Invalid number format: {e}")
print(result)  # Err('Invalid number format: ...')
```

### Collecting Results

```python
from rustico import Ok, Err

def process_items(items: list) -> list:
    results = [process_item(item) for item in items]
    
    # Filter out successful results
    successful = [result.unwrap() for result in results if result.is_ok()]
    
    # Collect errors
    errors = [result.unwrap_err() for result in results if result.is_err()]
    
    if errors:
        print(f"Warning: {len(errors)} items failed processing")
    
    return successful

def process_item(item):
    # Process the item and return Ok or Err
    pass
```

## Advanced Pattern Matching

!!! note "Python 3.10+ Feature"
    Pattern matching requires Python 3.10 or later. For earlier versions, use conditional checks with `is_ok()` and `is_err()`.

```python
from rustico import Ok, Err, as_result

@as_result(ValueError, ZeroDivisionError)
def divide(a: int, b: int) -> float:
    return a / b

result = divide(10, 0)

match result:
    case Ok(value):
        print(f"Result: {value}")
    case Err(ZeroDivisionError() as e):
        print(f"Division by zero error: {e}")
    case Err(ValueError() as e):
        print(f"Value error: {e}")
    case Err(e):
        print(f"Unexpected error: {e}")
```

## Working with External Libraries

!!! tip "Integration Pattern"
    When working with libraries that use exceptions, wrap their functions with `as_result` or use a try/except block that returns `Ok`/`Err`.

```python
from rustico import Ok, Err, Result
import requests

def fetch_data(url: str) -> Result[dict, Exception]:
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return Ok(response.json())
    except requests.RequestException as e:
        return Err(e)

# Usage
result = fetch_data("https://api.example.com/data")
data = result.unwrap_or({})
```

These examples demonstrate how `rustico` can be used in various real-world scenarios to make error handling more explicit, composable, and maintainable.

---

## Feature Comparison

| Feature | Traditional Try/Except | rustico |
| ------- | ---------------------- | ------- |
| Error Propagation | Manual re-raising | Automatic with `@do` |
| Error Information | Often lost in translation | Preserved exactly |
| Composability | Nested try/except blocks | Chainable operations |
| Type Safety | No static analysis | Full type hints |
| Pattern Matching | Not applicable | Native support |
| Readability | Often verbose and nested | Linear and clear |

---

## Next Steps

- [Read the Quick Start guide](quickstart.md) for more examples
- [Check the API Reference](rustico.md) for detailed documentation
- [Contribute to rustico](contributing.md) to help improve the library

[Back to Top](#examples){ .md-button }
