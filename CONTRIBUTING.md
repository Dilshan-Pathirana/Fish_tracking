# Contributing to FishTracker

Thank you for your interest in contributing to FishTracker! This document provides guidelines for contributing to the project.

## Getting Started

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Dilshan-Pathirana/Fish_tracking.git
   cd Fish_tracking
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in development mode with dev dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Verify installation:**
   ```bash
   pytest
   mypy .
   black --check .
   flake8 .
   ```

## Reporting Issues

### Bug Reports

Please use the [GitHub Issues](https://github.com/Dilshan-Pathirana/Fish_tracking/issues) tracker to report bugs.

When reporting a bug, include:
- Clear title and description
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Your environment (OS, Python version, dependency versions)
- Relevant screenshots or error messages
- A minimal reproducible example if possible

### Feature Requests

Feature requests are also tracked via [GitHub Issues](https://github.com/Dilshan-Pathirana/Fish_tracking/issues).

When requesting a feature, include:
- Clear title and motivation
- Use case and expected benefits
- Possible implementation approach (optional)
- Any relevant references or similar tools

## Code Contributions

### Before You Start

1. **Create an issue** for your proposed change (unless it's a trivial fix)
2. **Wait for feedback** to ensure alignment with project goals
3. **Fork the repository** and create a feature branch

### Code Style

All code must follow **PEP 8** style guidelines:

```bash
black .          # Format code automatically
flake8 .         # Check for style violations
```

### Type Hints

All functions must include **complete type hints**:

```python
def calculate_distance(points: List[Tuple[int, int]], scale: float = 1.0) -> float:
    """Calculate total distance from a list of (x, y) coordinates."""
    ...
```

### Documentation

Follow the documentation standard from *[Ten Simple Rules for Documenting Scientific Software](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007128)* (Lee et al., 2018):

1. **Module docstrings** — Explain what the module does
2. **Function/class docstrings** — Describe purpose, arguments, return values, and raises
3. **Inline comments** — Only for non-obvious logic
4. **No meta-comments** — Avoid "added for issue #X" or "used by Y flow"

Example docstring:
```python
"""Brief one-line description.

Longer explanation if needed.

Args:
    param_name (type): Description of parameter.

Returns:
    type: Description of return value.

Raises:
    ExceptionType: When this exception is raised.
"""
```

### Testing

1. **Write tests** for new functionality
   ```bash
   pytest tests/
   ```

2. **Maintain coverage** — Aim for ≥70% code coverage
   ```bash
   pytest --cov=utils
   ```

3. **Test structure** — Place tests in `tests/test_*.py` files

### Pull Request Process

1. **Update code and tests:**
   ```bash
   git checkout -b feature/your-feature-name
   # Make changes, add tests
   git add .
   git commit -m "Clear commit message describing changes"
   ```

2. **Run quality checks:**
   ```bash
   black .
   flake8 .
   mypy .
   pytest --cov=utils
   ```

3. **Push and create PR:**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **PR checklist:**
   - [ ] Code follows PEP 8 style
   - [ ] All functions have docstrings and type hints
   - [ ] Tests are included and pass
   - [ ] Coverage remains ≥70%
   - [ ] Commit messages are clear and descriptive
   - [ ] No breaking changes without discussion
   - [ ] Documentation is updated if needed

### Commit Messages

Write clear, descriptive commit messages:

✅ Good:
```
Add background subtraction preprocessing option

Implements MOG2 parameter tuning for improved detection in
low-contrast environments. Addresses #42.
```

❌ Poor:
```
fix stuff
update code
```

## Development Workflow

### Branch Naming
- `feature/` — New features
- `fix/` — Bug fixes
- `docs/` — Documentation improvements
- `refactor/` — Code refactoring

### CI/CD

All pull requests trigger automated checks:
- **Tests:** `pytest tests/`
- **Type checking:** `mypy .`
- **Code style:** `black --check .` and `flake8 .`

PRs must pass all checks before merging.

## Coding Conventions

### General Principles

1. **Simplicity first** — Don't over-engineer or add unnecessary abstractions
2. **Reuse existing patterns** — Follow established code patterns in the project
3. **Trust internal code** — Don't add error handling for cases that can't happen
4. **Validate at boundaries** — Only validate user input and external API responses
5. **Clear naming** — Use descriptive variable/function names

### Python-Specific

- Use modern type hints (Python 3.9+ syntax where possible)
- Avoid unnecessary comments — well-named code is self-documenting
- Keep functions small and focused
- Use standard library before external dependencies

## Questions?

- **Documentation:** Check the [README](README.md) and `docs/` folder
- **Discussions:** Open a [GitHub Discussion](https://github.com/Dilshan-Pathirana/Fish_tracking/discussions)
- **Email:** Reach out to the maintainer

## Code of Conduct

By contributing, you agree to uphold our [Code of Conduct](CODE_OF_CONDUCT.md).

## License

By contributing to FishTracker, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to make FishTracker better!** 🎣
