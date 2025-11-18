# Contributing to ISO 27001 Toolkit

Thank you for your interest in contributing to ISO 27001 Toolkit! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)

---

## 🤝 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of:
- Experience level
- Gender identity and expression
- Sexual orientation
- Disability
- Personal appearance
- Body size
- Race
- Ethnicity
- Age
- Religion
- Nationality

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- pip
- Virtual environment (recommended)

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/iso27001-toolbox.git
   cd iso27001-toolbox
   ```

3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/GitCroque/iso27001-toolbox.git
   ```

4. **Verify remotes**:
   ```bash
   git remote -v
   # origin    https://github.com/YOUR_USERNAME/iso27001-toolbox.git (fetch)
   # origin    https://github.com/YOUR_USERNAME/iso27001-toolbox.git (push)
   # upstream  https://github.com/GitCroque/iso27001-toolbox.git (fetch)
   # upstream  https://github.com/GitCroque/iso27001-toolbox.git (push)
   ```

---

## 🛠️ Development Setup

### 1. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Install package in editable mode with dev dependencies
pip install -e ".[dev]"

# Or install from requirements
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy
```

### 3. Install Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

### 4. Verify Installation

```bash
# Test CLI
iso27001 --version
iso27001 --help

# Run tests
pytest tests/ -v

# Check code style
black --check src/ tests/
flake8 src/ tests/
mypy src/
```

---

## 📝 How to Contribute

### Types of Contributions

We welcome the following types of contributions:

1. **🐛 Bug Reports** - Found a bug? Let us know!
2. **✨ Feature Requests** - Have an idea? Suggest it!
3. **📚 Documentation** - Improve docs, fix typos
4. **🧪 Tests** - Add or improve test coverage
5. **🔧 Code** - Fix bugs, implement features
6. **🌍 Translations** - Add support for new languages
7. **📝 Templates** - Add new policy templates

### Reporting Bugs

Before creating a bug report, please check existing issues. When creating a bug report, include:

**Template**:
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Run command '...'
2. With parameters '...'
3. See error

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment:**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.11.0]
- ISO 27001 Toolkit version: [e.g., 0.1.0]

**Additional context**
Any other context (logs, screenshots, etc.)
```

### Suggesting Features

Feature requests should include:

1. **Problem statement**: What problem does this solve?
2. **Proposed solution**: How should it work?
3. **Alternatives considered**: What other options did you think about?
4. **Use cases**: Who would use this feature?
5. **Implementation notes**: Any technical considerations?

**Template**:
```markdown
**Feature description**
A clear description of the feature.

**Use case**
Why is this feature needed? Who will benefit?

**Proposed implementation**
How should this work from a user perspective?

**Technical considerations**
Any architectural or technical notes.
```

---

## 💻 Coding Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

```python
# Line length: 100 characters (not 79)
# Use Black for formatting
# Use type hints

# Good ✅
def calculate_risk_score(impact: int, likelihood: int) -> tuple[int, str]:
    """
    Calculate risk score and level.

    Args:
        impact: Impact rating (1-5)
        likelihood: Likelihood rating (1-5)

    Returns:
        Tuple of (score, level)
    """
    score = impact * likelihood

    if score >= 16:
        level = "critical"
    elif score >= 10:
        level = "high"
    else:
        level = "medium"

    return score, level
```

### Code Style Rules

**Formatting**:
```bash
# Format code with Black
black src/ tests/ --line-length=100

# Check imports with isort
isort src/ tests/ --profile=black --line-length=100
```

**Linting**:
```bash
# Lint with flake8
flake8 src/ tests/ --max-line-length=100 --extend-ignore=E203,W503

# Type checking with mypy
mypy src/ --ignore-missing-imports
```

**Naming Conventions**:
- Classes: `PascalCase` (e.g., `RiskManager`)
- Functions/methods: `snake_case` (e.g., `calculate_risk_score`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `RISK_LEVEL_HIGH`)
- Private methods: `_leading_underscore` (e.g., `_generate_id`)

### Documentation

**Docstrings** (Google style):

```python
def add_risk(self, risk_data: Dict[str, Any]) -> str:
    """
    Add a new risk to the register.

    Args:
        risk_data: Dictionary containing risk information with keys:
            - name: Risk name (required)
            - description: Risk description (required)
            - category: Risk category (required)
            - impact: Impact rating 1-5 (required)
            - likelihood: Likelihood rating 1-5 (required)
            - treatment: Treatment strategy (optional)

    Returns:
        The generated risk ID (e.g., 'RISK-001')

    Raises:
        ValidationError: If risk_data is invalid
        DataPersistenceError: If save fails

    Example:
        >>> manager = RiskManager()
        >>> risk_id = manager.add_risk({
        ...     'name': 'Data breach',
        ...     'category': 'confidentiality',
        ...     'impact': 5,
        ...     'likelihood': 3
        ... })
        >>> print(risk_id)
        'RISK-001'
    """
```

### Import Organization

```python
# 1. Standard library
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# 2. Third-party packages
import click
import yaml
from rich.console import Console

# 3. Local imports
from iso27001_toolkit.exceptions import ValidationError
from iso27001_toolkit.utils.config import get_config_dir
```

---

## 🧪 Testing

### Test Requirements

- All new features **must** include tests
- Bug fixes **should** include regression tests
- Aim for **70%+ code coverage**
- Tests must pass before PR is merged

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=iso27001_toolkit --cov-report=html

# Run specific test file
pytest tests/utils/test_risk_manager.py -v

# Run specific test
pytest tests/utils/test_risk_manager.py::TestRiskManager::test_add_risk -v

# View coverage report
open htmlcov/index.html  # Mac/Linux
start htmlcov/index.html  # Windows
```

### Writing Tests

**File structure**:
```
tests/
├── conftest.py              # Shared fixtures
├── test_cli.py
├── commands/
│   ├── test_policies.py
│   ├── test_controls.py
│   ├── test_risks.py
│   └── test_audit.py
└── utils/
    ├── test_risk_manager.py
    ├── test_controls_tracker.py
    ├── test_encryption.py
    └── test_validators.py
```

**Example test**:

```python
import pytest
from iso27001_toolkit.utils.risk_manager import RiskManager
from iso27001_toolkit.exceptions import ValidationError


class TestRiskManager:
    """Tests for RiskManager class"""

    def test_add_risk_success(self, mock_config_dir, sample_risk_data):
        """Test adding a valid risk"""
        manager = RiskManager()
        risk_id = manager.add_risk(sample_risk_data)

        assert risk_id.startswith("RISK-")
        assert len(manager.get_all_risks()) == 1

    def test_add_risk_calculates_score(self, mock_config_dir):
        """Test risk score calculation"""
        manager = RiskManager()
        risk_id = manager.add_risk({
            'name': 'Test Risk',
            'category': 'confidentiality',
            'impact': 4,
            'likelihood': 3
        })

        risk = manager.get_risk(risk_id)
        assert risk['risk_score'] == 12  # 4 × 3
        assert risk['risk_level'] == 'high'

    def test_add_risk_invalid_data(self, mock_config_dir):
        """Test adding risk with invalid data"""
        manager = RiskManager()

        with pytest.raises(ValidationError):
            manager.add_risk({'name': ''})  # Empty name
```

**Using fixtures** (`conftest.py`):

```python
@pytest.fixture
def sample_risk_data():
    """Sample risk data for testing"""
    return {
        'name': 'Test Risk',
        'description': 'A test risk',
        'category': 'confidentiality',
        'assets': ['Server', 'Database'],
        'impact': 4,
        'likelihood': 3,
        'treatment': 'mitigate'
    }
```

---

## 🔄 Pull Request Process

### 1. Create a Branch

```bash
# Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name

# Or for bugfix
git checkout -b fix/bug-description
```

**Branch naming**:
- Features: `feature/feature-name`
- Bug fixes: `fix/bug-description`
- Documentation: `docs/what-you-changed`
- Tests: `test/what-you-tested`

### 2. Make Changes

```bash
# Make your changes
# ...

# Format code
black src/ tests/
isort src/ tests/

# Run tests
pytest tests/ -v

# Run pre-commit hooks
pre-commit run --all-files
```

### 3. Commit Changes

**Commit message format**:

```
type(scope): subject

body (optional)

footer (optional)
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples**:

```bash
# Good ✅
git commit -m "feat(risks): add export to Excel functionality"
git commit -m "fix(validators): prevent path traversal in sanitize_filename"
git commit -m "docs(README): add installation instructions for Windows"
git commit -m "test(controls): increase coverage to 80%"

# Bad ❌
git commit -m "fixed bug"
git commit -m "updates"
git commit -m "WIP"
```

**Detailed commit**:

```bash
git commit -m "feat(audit): add compliance report generation

- Add ComplianceReporter class
- Implement PDF export with reportlab
- Add tests for report generation
- Update documentation

Closes #42"
```

### 4. Push to Fork

```bash
# Push to your fork
git push origin feature/your-feature-name
```

### 5. Create Pull Request

1. Go to **your fork** on GitHub
2. Click **"New Pull Request"**
3. Select base: `main` ← compare: `feature/your-feature-name`
4. Fill in the PR template

### 6. Code Review

- Maintainers will review your PR
- Address feedback by pushing new commits
- Once approved, your PR will be merged

**During review**:
```bash
# Make requested changes
# ...

# Commit changes
git add .
git commit -m "refactor: address review feedback"

# Push to update PR
git push origin feature/your-feature-name
```

---

## 🙏 Thank You!

Thank you for contributing to ISO 27001 Toolkit! Your efforts help organizations improve their information security posture. 🔒

**Questions?** Open an issue or start a discussion on GitHub.

---

**Last Updated**: 2025-11-18
**Version**: 0.1.0
