# Development Guide for PyEMD

This guide covers the development setup, build system, and workflows for contributing to PyEMD.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) >= 0.9.18 - Fast Python package installer and resolver
- Git
- C++ compiler (gcc, clang, or MSVC depending on platform)
- [Ninja](https://ninja-build.org/) build system (usually auto-installed by meson-python)

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

### **meson-python** (Build Backend)
- Modern build backend for Python packages with compiled extensions
- Replaced setuptools for better performance and cleaner configuration
- Automatically handles Cython → C++ compilation
- Configuration in `meson.build`

### **Meson** (Build System)
- Cross-platform build system that handles the actual C++/Cython compilation
- Fast, parallel builds with Ninja backend
- Cleaner than setuptools for compiled extensions

### **uv** (Package Manager)
- Fast Python package installer and resolver
- Manages dependencies via `pyproject.toml` and locks them in `uv.lock`
- Replaces pip/conda for development

## Key Files

- **`pyproject.toml`**: Python package metadata, dependencies, and build configuration
- **`meson.build`**: Build instructions for Meson (how to compile the extension)
- **`uv.lock`**: Locked dependency versions for reproducible builds
- **`Makefile`**: Convenient shortcuts for common development tasks
- **`setup.py.deprecated`**: Old setuptools config (kept for reference only)

## Building

### Local Development Build

Build wheels and source distributions:
```bash
uv build
```

This creates:
- `dist/pyemd-*.whl` - Binary wheel for your platform
- `dist/pyemd-*.tar.gz` - Source distribution (requires git)

### Building for Multiple Platforms

Use `cibuildwheel` to build wheels for Linux, macOS, and Windows:
```bash
uv run cibuildwheel --platform linux
```

Or use the Makefile shortcut:
```bash
make dist-build-wheels
```

## Development Workflow

### Install Dependencies

```bash
uv sync --all-extras
```

This installs:
- Runtime dependencies (numpy)
- Test dependencies (pytest)
- Distribution tools (build, cibuildwheel, twine)
- Development tools (ipython)

### Development Workflow

This project uses a wheel-based development workflow. The `Makefile` automates the build and installation process:

```bash
# One-time setup: build and install
make develop

# Run tests
make test

# Or run tests manually
.venv/bin/pytest
```

You can also use `uv run` for quick commands:
```bash
uv run python -c "import pyemd; print(pyemd.__version__)"
uv run pytest
```

**After making code changes:**

```bash
make develop  # Rebuild and reinstall
make test     # Run tests
```

Or manually:
```bash
make clean
uv build --wheel
uv pip install --force-reinstall --no-deps dist/pyemd-*.whl
.venv/bin/pytest
```

**Why wheel-based development?**

For packages with C++ extensions like pyemd, wheel-based development is the most reliable approach because:
- No rebuild-on-import overhead
- No dependency on build directory structure at runtime
- Clearer separation between build and runtime
- Avoids PATH issues with build tools in subprocesses

Meson-python's editable installs use a rebuild-on-import mechanism that requires build tools (cython, ninja) to be available in the system PATH whenever Python starts. This creates environment issues because the rebuild runs in a subprocess that doesn't inherit the virtualenv's PATH.

We've configured `package = false` in `pyproject.toml` to prevent automatic editable installs, which allows `uv run` to work with the installed wheel.

### Clean Build Artifacts

```bash
make clean
```

This removes:
- `__pycache__` directories
- Compiled extensions (`.so`, `.dylib`)
- Build directories (`build/`, `.mesonpy-*`)
- Egg info

## Dependency Management

Dependencies are managed in `pyproject.toml` and locked in `uv.lock`.

### Add a Dependency

1. Edit `pyproject.toml`:
   ```toml
   [project]
   dependencies = ["numpy >= 1.9.0", "new-package >= 1.0"]
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

## Making Changes

### Modifying Python Code

Python changes in `src/pyemd/__init__.py` or `src/pyemd/emd.pyx` require rebuilding:

```bash
uv build --wheel
uv pip install --force-reinstall dist/pyemd-*.whl
uv run pytest
```

### Modifying C++ Code

Changes to C++ headers in `src/pyemd/lib/` require a full rebuild:

```bash
make clean
uv build --wheel
uv pip install --force-reinstall dist/pyemd-*.whl
uv run pytest
```

### Modifying Build Configuration

Changes to `meson.build` or `pyproject.toml` [build-system] section:

```bash
make clean
uv sync  # Rebuild with new config
```

## Versioning

PyEMD uses [setuptools_scm](https://setuptools-scm.readthedocs.io/) for git-based versioning:

- Version is automatically derived from git tags
- Development versions include commit hash (e.g., `0.5.1.dev87+g255824f`)
- Release versions match git tags (e.g., `0.5.1`)

To create a release:
```bash
git tag v0.5.2
git push --tags
```

## Release Process

1. **Ensure all changes are committed**:
   ```bash
   git status
   ```

2. **Run tests**:
   ```bash
   make test
   ```

3. **Build locally** to verify:
   ```bash
   make dist-build-local
   ```

4. **Tag the release**:
   ```bash
   git tag v0.5.2
   git push --tags
   ```

5. **GitHub Actions will automatically build wheels** for all platforms

6. **Download artifacts from GitHub Actions**

7. **Sign and upload to PyPI**:
   ```bash
   make dist-sign
   make dist-upload
   ```

## Continuous Integration

### GitHub Actions Workflows

**`build_wheels.yml`**:
- Builds wheels for Linux, Windows, and macOS
- Uses `cibuildwheel` with uv as build frontend
- Runs on every push and pull request
- Artifacts uploaded as build artifacts

**`make_sdist.yml`**:
- Builds source distribution
- Requires git history for version detection
- Uploads to GitHub Actions artifacts

### Local Testing of CI

Test wheel building locally:
```bash
uv run cibuildwheel --platform linux --config-file pyproject.toml
```

## Troubleshooting

### Build Failures

**"No module named 'pyemd'"**:
- The package needs to be rebuilt and installed after changes
- Run: `uv build --wheel && uv pip install --force-reinstall dist/pyemd-*.whl`

**"meson-python editable install failed"**:
- Editable installs with meson-python have limitations
- Use wheel installs for development instead
- See: https://mesonbuild.com/meson-python/how-to-guides/editable-installs.html

**"setuptools_scm version not found"**:
- Ensure you cloned with full git history: `git fetch --unshallow`
- Or set an environment variable: `SETUPTOOLS_SCM_PRETEND_VERSION=0.5.1`

**Compiler warnings about sign comparison**:
- These are from the upstream C++ library code
- They're non-fatal and don't affect functionality
- Can be safely ignored

### Dependency Issues

**"Command 'uv' not found"**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Then restart your terminal
```

**"ninja not found"**:
- Usually auto-installed by meson-python
- Manual install: `brew install ninja` (macOS) or `apt install ninja-build` (Ubuntu)

## Getting Help

- **Issues**: https://github.com/wmayner/pyemd/issues
- **meson-python docs**: https://mesonbuild.com/meson-python/
- **uv docs**: https://docs.astral.sh/uv/

## Architecture Overview

```
pyemd/
├── src/pyemd/
│   ├── __init__.py         # Python API
│   ├── emd.pyx             # Cython wrapper
│   └── lib/                # C++ implementation (header-only)
│       ├── emd_hat.hpp     # Main EMD algorithm
│       └── ...             # Supporting headers
├── test/                   # Test suite
├── meson.build             # Build configuration
├── pyproject.toml          # Project metadata & dependencies
└── uv.lock                 # Locked dependencies

Build flow:
1. meson-python reads meson.build
2. Meson compiles emd.pyx → emd.cpp (via Cython)
3. C++ compiler builds emd.cpp + lib/*.hpp → emd.so
4. Wheel packaged with Python files
```

## References

- [Scientific Python Development Guide - Compiled Packaging](https://learn.scientific-python.org/development/guides/packaging-compiled/)
- [NumPy 1.26.0 Release Notes](https://numpy.org/doc/stable/release/1.26.0-notes.html) (meson-python migration)
- [Meson-Python Documentation](https://mesonbuild.com/meson-python/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [PEP 517](https://peps.python.org/pep-0517/) - Build system interface
- [PEP 518](https://peps.python.org/pep-0518/) - pyproject.toml specification
