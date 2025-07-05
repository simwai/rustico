# Installation

Installing `rustico` is simple and straightforward. You can install it using pip, PDM, or Poetry.

## Using pip

```bash
pip install rustico
```

## Using PDM

```bash
pdm add rustico
```

## Using Poetry

```bash
poetry add rustico
```

## Verifying Installation

You can verify that `rustico` is installed correctly by running the following Python code:

```python
from rustico import Ok, Err

result = Ok(42)
print(result)  # Should print: Ok(42)
```

## Requirements

- Python 3.8 or higher
- No additional dependencies required

## Development Installation

If you want to contribute to `rustico`, you can install it in development mode:

```bash
git clone https://github.com/simwai/rustico.git
cd rustico
pdm install
```
