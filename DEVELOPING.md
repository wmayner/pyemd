# Development Guide for PyEMD

This guide covers the development setup, build system, and workflows for contributing to PyEMD.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) - Fast Python package installer and resolver
- Git
- Python 3.12+

No compiler is required—PyEMD v2.0+ is a pure Python package.

## Quick Start

1. **Clone the repository with full history** (needed for version detection):
   ```bash
   git clone https://github.com/wmayner/pyemd.git
   cd pyemd
   ```

2. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Set up the development environment**:
   ```bash
   uv sync --all-extras
   ```

This installs all dependencies (including test and distribution tools) and creates a virtual environment at `.venv/`.

## Build System

PyEMD uses modern Python packaging tools:

### **setuptools** (Build Backend)
- Standard Python build backend
- Configuration in `pyproject.toml`
- Produces universal wheels (`py3-none-any`)

### **setuptools_scm** (Version Management)
- Automatically derives version from git tags
- No manual version bumping required

### **uv** (Package Manager)
- Fast Python package installer and resolver
- Manages dependencies via `pyproject.toml` and locks them in `uv.lock`

## Key Files

- **`pyproject.toml`**: Python package metadata, dependencies, and build configuration
- **`uv.lock`**: Locked dependency versions for reproducible builds
- **`Makefile`**: Convenient shortcuts for common development tasks

## Building

### Local Development Build

Build wheels and source distributions:
```bash
uv build
```

This creates:
- `dist/pyemd-*-py3-none-any.whl` - Universal wheel (works on all platforms)
- `dist/pyemd-*.tar.gz` - Source distribution

### Editable Install

For development, install in editable mode:
```bash
uv pip install -e .
```

Changes to Python code are immediately reflected without reinstalling.

## Development Workflow

### Install Dependencies

```bash
uv sync --all-extras
```

This installs:
- Runtime dependencies (numpy, pot)
- Test dependencies (pytest)
- Distribution tools (build, twine, towncrier)
- Development tools (ipython)

### Run Tests

```bash
make test
# or
uv run pytest
```

### Make Changes

1. Edit Python code in `src/pyemd/`
2. Run tests: `uv run pytest`
3. Commit changes

For pure Python packages, no rebuild step is needed between code changes and testing when using editable installs.

### Clean Build Artifacts

```bash
make clean
```

## Dependency Management

Dependencies are managed in `pyproject.toml` and locked in `uv.lock`.

### Add a Dependency

1. Edit `pyproject.toml`:
   ```toml
   [project]
   dependencies = ["numpy >= 1.15.0", "pot >= 0.9.0", "new-package >= 1.0"]
   ```

2. Update the lockfile:
   ```bash
   uv sync
   ```

3. Commit both `pyproject.toml` and `uv.lock`

### Update Dependencies

Update all dependencies to their latest compatible versions:
```bash
uv sync --upgrade
```

Update a specific package:
```bash
uv sync --upgrade-package numpy
```

**Always commit `uv.lock` after updating dependencies** to ensure reproducible builds.

## Testing

### Run All Tests

```bash
uv run pytest
```

### Run Specific Test

```bash
uv run pytest test/test_pyemd.py::test_emd_1 -v
```

### Run Tests with Coverage

```bash
uv run pytest --cov=pyemd --cov-report=html
```

## Versioning

PyEMD uses [setuptools_scm](https://setuptools-scm.readthedocs.io/) for git-based versioning:

- Version is automatically derived from git tags
- Development versions include commit info (e.g., `2.0.0.dev5+gabcdef`)
- Release versions match git tags (e.g., `2.0.0`)

To create a release:
```bash
git tag v2.0.0
git push --tags
```

## Changelog Management

PyEMD uses [towncrier](https://towncrier.readthedocs.io/) for changelog management.

### Create a Changelog Fragment

For each change, create a file in `changelog.d/`:

```bash
# With issue number
echo "Fixed the thing" > changelog.d/123.bugfix

# Without issue number (use + prefix)
echo "Added new feature" > changelog.d/+new-feature.feature
```

Fragment types: `.feature`, `.bugfix`, `.doc`, `.removal`, `.misc`

### Preview Changelog

```bash
uv run towncrier build --draft --version 2.0.0
```

### Build Changelog for Release

```bash
uv run towncrier build --version 2.0.0
```

This updates `CHANGELOG.rst` and removes the fragment files.

## Release Process

1. **Ensure all changes are committed**:
   ```bash
   git status
   ```

2. **Run tests**:
   ```bash
   make test
   ```

3. **Build changelog**:
   ```bash
   uv run towncrier build --version X.Y.Z
   git add CHANGELOG.rst changelog.d/
   git commit -m "Update changelog for vX.Y.Z"
   ```

4. **Tag the release**:
   ```bash
   git tag vX.Y.Z
   git push origin main --tags
   ```

5. **Build and upload to PyPI**:
   ```bash
   uv build
   uv run twine upload dist/*
   ```

## Continuous Integration

### GitHub Actions Workflows

**`build_wheels.yml`**:
- Runs tests on Python 3.12 and 3.13
- Builds universal wheel and source distribution
- Uploads artifacts

### Local Testing

```bash
# Build wheel
uv build --wheel

# Test the built wheel
uv run --isolated --with dist/pyemd-*.whl python -c "import pyemd; print(pyemd.__version__)"
```

## Troubleshooting

### Build Failures

**"setuptools_scm version not found"**:
- Ensure you cloned with full git history: `git fetch --unshallow`
- Or set an environment variable: `SETUPTOOLS_SCM_PRETEND_VERSION=2.0.0`

### Dependency Issues

**"Command 'uv' not found"**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Then restart your terminal
```

## Getting Help

- **Issues**: https://github.com/wmayner/pyemd/issues
- **uv docs**: https://docs.astral.sh/uv/

## Architecture Overview

```
pyemd/
├── src/pyemd/
│   ├── __init__.py    # Package exports and version
│   └── emd.py         # Pure Python EMD implementation (uses POT)
├── test/
│   └── test_pyemd.py  # Test suite
├── pyproject.toml     # Project metadata & dependencies
└── uv.lock            # Locked dependencies
```

PyEMD v2.0 is a pure Python package that uses the [POT library](https://pythonot.github.io/) (Python Optimal Transport) for computing Earth Mover's Distance.

## References

- [Python Packaging User Guide](https://packaging.python.org/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [setuptools_scm Documentation](https://setuptools-scm.readthedocs.io/)
- [towncrier Documentation](https://towncrier.readthedocs.io/)
- [PEP 517](https://peps.python.org/pep-0517/) - Build system interface
- [PEP 518](https://peps.python.org/pep-0518/) - pyproject.toml specification
