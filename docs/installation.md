# Installation

`rustico` is distributed on two Python package repositories:

- **[PyPI](https://pypi.org/project/rustico/)** — the main, production distribution
- **[TestPyPI](https://test.pypi.org/project/rustico/)** — the test distribution, used to verify new releases before they go live

Both are installed with `pip`; they only differ in which index you point at.

## From PyPI (main distribution)

Requires Python 3.8 or newer:

```bash
pip install rustico
```

## From TestPyPI (test distribution)

TestPyPI hosts every uploaded version, including releases that may still be under review. Always pin an exact version so you install the release you intend to test:

```bash
pip install rustico==X.Y.Z --index-url https://test.pypi.org/simple/
```

!!! warning
    TestPyPI is for **testing only**. Packages there can be overwritten or deleted, and it is not a stable distribution channel. Never rely on TestPyPI in production.

## Index selection: `--index-url` vs `--extra-index-url`

- `--index-url https://test.pypi.org/simple/` — use **only** TestPyPI. This is the right choice for `rustico`, which has no runtime dependencies.
- `--extra-index-url https://test.pypi.org/simple/` — keep PyPI as the default and search TestPyPI *in addition*. Use this if a test release ever depends on other packages that only exist on TestPyPI.

## Browsing the distributions

- Main: <https://pypi.org/project/rustico/>
- Test: <https://test.pypi.org/project/rustico/>
