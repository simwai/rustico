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
3. Use [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, ...) so the changelog is generated correctly
4. Submit a pull request with a clear description of the changes
5. Address any feedback from code reviews

## Release Process

Releases are managed by the maintainers and run from the `main` branch. The changelog and version number are handled automatically by [python-semantic-release](https://python-semantic-release.readthedocs.io/), which reads Conventional Commit messages to determine the next version (see [VERSIONING.md](https://github.com/simwai/rustico/blob/main/VERSIONING.md)).

Releases follow Semantic Versioning:

- `feat:` commits bump the **minor** version
- `fix:` commits bump the **patch** version
- Breaking changes (a `BREAKING CHANGE:` footer or a `!` after the type) bump the **major** version

Before releasing, make sure your local `~/.pypirc` is configured with both a `testpypi` and a `pypi` repository (upload credentials are read from there).

### Preview the next version

```bash
pdm psr-print
```

Prints the next version that would be released, without changing anything.

### Release

```bash
pdm release
```

This runs in one go:

1. `python-semantic-release version` — computes the next version from commits, bumps it in `pyproject.toml`, regenerates `CHANGELOG.md` from the git history, creates a release commit and tag (`vX.Y.Z`), and pushes them to `main`
2. Builds the distribution and uploads it to **TestPyPI** first
3. Uploads the same build to **PyPI**

Optionally create a GitHub Release from the pushed tag with the changelog notes. If you export a `GH_TOKEN` locally, python-semantic-release will create it automatically.

### TestPyPI verification only

If you only want to smoke-test a build on TestPyPI (no version bump):

```bash
pdm test-publish
```

### Configuration

Version management lives in `[tool.semantic_release]` in `pyproject.toml`. The `CHANGELOG.md` is generated in `init` mode (rebuilt from git history on every release), so never edit it manually.

## Code of Conduct

Please be respectful and considerate of others when contributing to the project. We aim to foster an inclusive and welcoming community.

## License

By contributing to `rustico`, you agree that your contributions will be licensed under the project's MIT license.
