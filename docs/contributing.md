# Contributing to rustico

Thank you for your interest in contributing to `rustico`! This document provides guidelines and instructions for contributing to the project.

## Development Environment Setup

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment:

```bash
# Install PDM if you don't have it
pip install pdm

# Install development dependencies
pdm install
```

## Development Workflow

1. Create a new branch for your feature or bugfix:

```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and write tests for them
3. Run the tests to ensure everything works:

```bash
pdm test
```

4. Format your code:

```bash
pdm format
```

5. Commit your changes with a descriptive commit message
6. Push your branch to your fork
7. Create a pull request to the main repository

## Code Style

We follow PEP 8 guidelines with a few modifications. The project uses Ruff for linting and formatting.

Key style points:

- Use type hints for all function parameters and return values
- Write docstrings for all public functions, classes, and methods
- Keep lines under 100 characters
- Use descriptive variable names

## Testing

All new features should include tests. We use pytest for testing.

- Write unit tests for all new functionality
- Ensure all tests pass before submitting a pull request
- Aim for high test coverage

## Documentation

Documentation is crucial for `rustico`. When adding new features:

- Update docstrings with clear explanations and examples
- Add type hints that work well with static type checkers
- Consider adding examples to the documentation

## Pull Request Process

1. Ensure your code passes all tests
2. Update the documentation if needed
3. Add your changes to the CHANGELOG.md file
4. Submit a pull request with a clear description of the changes
5. Address any feedback from code reviews

## Release Process

Releases are managed by the maintainers. The general process is:

1. Update version in pyproject.toml
2. Update CHANGELOG.md
3. Create a new release on GitHub
4. Publish to PyPI

## Code of Conduct

Please be respectful and considerate of others when contributing to the project. We aim to foster an inclusive and welcoming community.

## License

By contributing to `rustico`, you agree that your contributions will be licensed under the project's MIT license.
