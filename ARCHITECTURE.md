# Architecture - ISO 27001 Toolkit

## 📐 Overview

ISO 27001 Toolkit follows a **layered architecture** pattern with clear separation of concerns. This document provides detailed architectural insights for developers and contributors.

**Version**: 0.1.0
**Last Updated**: 2025-11-18
**Architecture Pattern**: Layered (N-tier)

---

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  CLI Layer (Click)                       │
│  Commands: policies, controls, risks, audit              │
│  Responsibilities: User interaction, argument parsing    │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│            Business Logic Layer                          │
│  Managers: RiskManager, ControlsTracker, AuditHelper    │
│  Utilities: TemplateEngine, Validators                  │
│  Responsibilities: Business rules, data transformation   │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│          Data Access Layer                               │
│  Storage: YAMLStorage (abstract), EncryptionManager     │
│  Responsibilities: Data persistence, encryption          │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│              Data Layer                                  │
│  YAML files, Templates (Jinja2), Static data            │
│  Responsibilities: Data storage                          │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Project Structure

```
iso27001-toolbox/
│
├── src/iso27001_toolkit/          # Main package (3232 LOC)
│   │
│   ├── cli.py                      # CLI entry point
│   ├── __init__.py                 # Package initialization + version
│   ├── constants.py                # Business constants
│   ├── exceptions.py               # Exception hierarchy
│   ├── logger.py                   # Logging configuration
│   ├── validators.py               # Input validation (13 functions)
│   │
│   ├── commands/                   # CLI command groups
│   │   ├── __init__.py
│   │   ├── policies.py             # Policy generation commands
│   │   ├── controls.py             # Controls tracking commands
│   │   ├── risks.py                # Risk management commands
│   │   └── audit.py                # Audit preparation commands
│   │
│   ├── utils/                      # Utility modules
│   │   ├── __init__.py
│   │   ├── base_storage.py         # Abstract YAML storage
│   │   ├── config.py               # Configuration management
│   │   ├── encryption.py           # Fernet encryption
│   │   ├── template_engine.py      # Jinja2 rendering
│   │   ├── controls_data.py        # 114 controls data (static)
│   │   ├── controls_tracker.py     # Controls state tracking
│   │   ├── risk_manager.py         # Risk CRUD operations
│   │   └── audit_helper.py         # Audit utilities
│   │
│   └── templates/                  # Jinja2 templates
│       ├── policies/               # 11+ security policies
│       ├── risks/                  # Risk assessment reports
│       └── audit/                  # Audit checklists, SOA
│
├── tests/                          # Test suite (pytest)
│   ├── conftest.py                 # Shared fixtures
│   ├── test_cli.py                 # CLI tests
│   ├── commands/                   # Command tests
│   └── utils/                      # Utility tests
│
├── examples/                       # Usage examples
│   ├── config.example.yml
│   └── quickstart.sh
│
├── pyproject.toml                  # Project metadata + deps
├── setup.py                        # Setuptools config
├── requirements.txt                # Dependencies
├── README.md                       # User documentation
├── SECURITY.md                     # Security policy
├── CONTRIBUTING.md                 # Contribution guide
└── AUDIT_REPORT.md                 # Security audit report
```

---

## 🔧 Core Components

### 1. CLI Layer (`cli.py`)

**Technology**: Click framework
**Responsibilities**:
- Parse command-line arguments
- Route commands to appropriate handlers
- Handle user input/output with Rich library

**Command Hierarchy**:

```
iso27001
├── info                           # Display toolkit information
├── policies                       # Policy management
│   ├── list                       # List available policies
│   ├── configure                  # Configure organization
│   └── generate                   # Generate policies
├── controls                       # Controls tracking
│   ├── init                       # Initialize tracker
│   ├── list                       # List all controls
│   ├── show <ID>                  # Show control details
│   ├── update <ID>                # Update control
│   └── report                     # Generate report
├── risks                          # Risk management
│   ├── init                       # Initialize register
│   ├── list                       # List all risks
│   ├── show <ID>                  # Show risk details
│   ├── add                        # Add new risk
│   ├── update <ID>                # Update risk
│   ├── report                     # Generate report
│   └── matrix                     # Display risk matrix
└── audit                          # Audit preparation
    ├── readiness                  # Assess readiness
    ├── checklist                  # Generate checklist
    ├── gap-analysis               # Gap analysis
    ├── generate-soa               # Generate SOA
    ├── prepare-evidence           # Prepare evidence
    └── schedule <date>            # Schedule audit
```

**Example Implementation**:

```python
@click.group()
@click.version_option(version=__version__)
def main():
    """ISO 27001 Toolkit - Main CLI"""
    pass

@main.command()
def info():
    """Display information"""
    console.print(Panel.fit(...))
```

---

### 2. Business Logic Layer

#### 2.1 RiskManager (`utils/risk_manager.py`)

**Responsibilities**:
- CRUD operations on risks
- Risk score calculation (impact × likelihood)
- Risk level determination (critical/high/medium/low)
- Statistics generation

**Key Methods**:

```python
class RiskManager:
    def __init__(self):
        self.file_path = get_risks_file()
        self.data = self._load()

    def add_risk(self, risk_data: Dict) -> str:
        """Add a new risk with auto-generated ID"""
        risk_id = self._generate_risk_id()  # RISK-001, RISK-002, ...
        score, level = self._calculate_risk_score(impact, likelihood)
        # ...
        return risk_id

    def _calculate_risk_score(self, impact: int, likelihood: int) -> tuple:
        """Calculate risk score and level"""
        score = impact * likelihood  # 1-25

        if score >= 16:
            level = 'critical'
        elif score >= 10:
            level = 'high'
        elif score >= 5:
            level = 'medium'
        else:
            level = 'low'

        return score, level

    def get_statistics(self) -> Dict:
        """Return statistics by level, status, treatment"""
```

**Risk Matrix (5×5)**:

```
        Impact →
      1    2    3    4    5
    ┌────┬────┬────┬────┬────┐
  5 │ M  │ M  │ H  │ H  │ C  │
P 4 │ L  │ M  │ M  │ H  │ C  │
r 3 │ L  │ L  │ M  │ H  │ H  │
o 2 │ L  │ L  │ M  │ M  │ M  │
b 1 │ L  │ L  │ L  │ M  │ M  │
    └────┴────┴────┴────┴────┘

L = Low (1-4)
M = Medium (5-9)
H = High (10-15)
C = Critical (16-25)
```

#### 2.2 ControlsTracker (`utils/controls_tracker.py`)

**Responsibilities**:
- Track implementation status of 114 ISO 27001:2022 controls
- Store evidence and notes
- Generate progress reports

**Control States**:
- `not_started` - Not yet started
- `in_progress` - Implementation ongoing
- `implemented` - Fully implemented
- `verified` - Verified by audit

**Key Methods**:

```python
class ControlsTracker(YAMLStorage):
    def update_control_status(self, control_id: str, status: str):
        """Update control implementation status"""

    def add_control_evidence(self, control_id: str, evidence: List[str]):
        """Add implementation evidence"""

    def get_control_status(self, control_id: str) -> str:
        """Get current status"""

    def get_implementation_percentage(self) -> float:
        """Calculate % of implemented controls"""
```

#### 2.3 AuditHelper (`utils/audit_helper.py`)

**Responsibilities**:
- Assess audit readiness
- Generate Statement of Applicability (SOA)
- Create gap analysis reports
- Prepare evidence packages

**Key Methods**:

```python
class AuditHelper:
    def assess_readiness(self) -> Dict:
        """
        Returns:
            {
                'percentage': float,  # 0-100
                'level': str,         # excellent/good/fair/poor
                'implemented': int,
                'total': int
            }
        """

    def generate_soa(self) -> str:
        """Generate Statement of Applicability (Markdown)"""

    def gap_analysis(self) -> List[Dict]:
        """Identify gaps in implementation"""
```

**Readiness Levels**:
- **Excellent** (≥90%): Ready for certification audit
- **Good** (≥75%): Minor gaps, ready for pre-audit
- **Fair** (≥60%): Significant work needed
- **Poor** (<60%): Not ready for audit

#### 2.4 TemplateEngine (`utils/template_engine.py`)

**Technology**: Jinja2
**Responsibilities**:
- Render policy templates
- Generate reports (MD, YAML)
- Variable substitution

**Template Variables**:

```python
context = {
    'organization_name': str,
    'organization_address': str,
    'ciso_name': str,
    'ciso_email': str,
    'dpo_name': str,
    'dpo_email': str,
    'effective_date': str,
    'review_period': str,
    'current_date': str,
    # ... custom variables
}
```

**Example Template** (`templates/policies/information_security_policy.md`):

```jinja2
# {{ organization_name }} - Information Security Policy

**Effective Date**: {{ effective_date }}
**Review Period**: {{ review_period }}
**CISO**: {{ ciso_name }} ({{ ciso_email }})

## 1. Purpose
...
```

#### 2.5 Validators (`validators.py`)

**Responsibilities**:
- Validate all user inputs
- Prevent injection attacks
- Sanitize file paths

**13 Validation Functions**:

```python
validate_email(email: str) -> str
validate_date(date_str: str, format: str) -> datetime
validate_risk_score(score: Any, min_val: int, max_val: int) -> int
validate_choice(value: str, choices: List[str]) -> str
validate_non_empty(value: str, field_name: str) -> str
validate_integer_range(value: Any, min_val: int, max_val: int) -> int
validate_url(url: str) -> str
validate_file_path(path: str, must_exist: bool) -> Path
validate_control_id(control_id: str) -> str
validate_percentage(value: Any) -> float
sanitize_filename(filename: str) -> str  # ⚠️ Security-critical
```

**Security Example**:

```python
def sanitize_filename(filename: str) -> str:
    """Prevent path traversal attacks"""
    # Remove dangerous characters: <>/\|?*
    # Remove control characters: \x00-\x1f
    sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', filename)

    if not sanitized:
        raise ValidationError("Invalid filename")

    return sanitized
```

---

### 3. Data Access Layer

#### 3.1 YAMLStorage (Abstract Base Class)

**Pattern**: Template Method
**Responsibilities**:
- Abstract YAML persistence
- Backup/restore functionality
- Optional encryption support

```python
class YAMLStorage:
    """Abstract base class for YAML storage"""

    def __init__(self, file_path: Path, encrypt: bool = False):
        self.file_path = file_path
        self.encrypt = encrypt
        self.data = {}
        self.encryption_manager = None

    def _get_default_data(self) -> Dict:
        """Override in subclasses"""
        return {'last_updated': None}

    def load(self) -> Dict:
        """Load data from YAML file"""
        if self.encrypt and self.encryption_manager:
            content = self.encryption_manager.decrypt(content)
        return yaml.safe_load(content)

    def save(self) -> None:
        """Save data to YAML file"""
        if self.encrypt and self.encryption_manager:
            content = self.encryption_manager.encrypt(content)
        # Write to file

    def backup(self, backup_path: Path = None) -> Path:
        """Create timestamped backup"""

    def restore(self, backup_path: Path) -> None:
        """Restore from backup"""

    def clear(self) -> None:
        """Reset to default data"""
```

**Child Classes**:
- `ControlsTracker` → `~/.iso27001/data/controls.yml`
- `RiskManager` → `~/.iso27001/data/risks.yml`
- `AuditHelper` → `~/.iso27001/data/audit.yml`

#### 3.2 EncryptionManager (`utils/encryption.py`)

**Technology**: Fernet (cryptography library)
**Algorithm**: AES-128-CBC + HMAC-SHA256
**Responsibilities**:
- Encrypt/decrypt sensitive data
- Key generation and management
- File-level encryption

```python
class EncryptionManager:
    def __init__(self, key_file: Path = None):
        self.key_file = key_file or Path.home() / ".iso27001" / "encryption.key"
        self.key = self._load_or_generate_key()
        self.cipher = Fernet(self.key)

    def _generate_key(self) -> bytes:
        """Generate and save Fernet key with 0o600 permissions"""
        key = Fernet.generate_key()
        with open(self.key_file, 'wb') as f:
            f.write(key)
        os.chmod(self.key_file, 0o600)  # Read/write for owner only
        return key

    def encrypt(self, data: Union[str, bytes]) -> str:
        """Encrypt data to base64 string"""
        return self.cipher.encrypt(data).decode('utf-8')

    def decrypt(self, encrypted_data: Union[str, bytes]) -> str:
        """Decrypt from base64 string"""
        return self.cipher.decrypt(encrypted_data).decode('utf-8')

    def encrypt_file(self, input_file: Path) -> Path:
        """Encrypt entire file"""

    def rotate_key(self) -> None:
        """Generate new key (requires re-encryption of all data)"""
```

**Security Notes**:
- Key stored in plaintext (Fernet limitation)
- File permissions prevent unauthorized access
- Backup key securely before rotation

---

### 4. Data Layer

#### 4.1 File Storage Structure

```
~/.iso27001/
├── config.yml                      # Organization configuration
│   ├── organization_name
│   ├── ciso_name, ciso_email
│   ├── dpo_name, dpo_email
│   ├── effective_date
│   └── review_period
│
├── data/                           # Runtime data
│   ├── controls.yml                # Controls tracking
│   │   └── controls:
│   │       A.5.1:
│   │         status: implemented
│   │         priority: high
│   │         notes: "..."
│   │         evidence: [...]
│   │         implementation_date: ISO8601
│   │
│   ├── risks.yml                   # Risk register
│   │   └── risks: []
│   │       - id: RISK-001
│   │         name: "..."
│   │         category: confidentiality
│   │         impact: 4
│   │         likelihood: 3
│   │         risk_score: 12
│   │         risk_level: high
│   │         status: analyzed
│   │         treatment: mitigate
│   │         controls: [A.5.15, A.5.16]
│   │
│   └── audit.yml                   # Audit data
│       └── scheduled_audits: []
│           last_assessment: ISO8601
│           readiness_score: float
│
├── logs/                           # Application logs
│   └── iso27001_toolkit.log        # Rotating logs (5 × 5MB)
│
└── encryption.key                  # Fernet encryption key (0o600)
```

#### 4.2 Static Data (`controls_data.py`)

**ISO 27001:2022 Annexe A - 114 Controls**:

```python
CONTROLS = {
    'A.5': {
        'name': 'Contrôles organisationnels',
        'count': 37,
        'controls': [
            {
                'id': 'A.5.1',
                'name': 'Politiques de sécurité de l\'information',
                'category': 'A.5',
                'type': 'Organizational',
                'description': '...',
                'purpose': '...'
            },
            # ... 36 more
        ]
    },
    'A.6': {'name': 'Contrôles des personnes', 'count': 8},
    'A.7': {'name': 'Contrôles physiques', 'count': 14},
    'A.8': {'name': 'Contrôles technologiques', 'count': 34},
}
```

**Total**: 37 + 8 + 14 + 34 = **114 controls**

---

## 🔄 Data Flow Diagrams

### Policy Generation Flow

```
User: iso27001 policies generate -p information_security_policy
  │
  ├─→ CLI (policies.py)
  │     │
  │     ├─→ Load config: ConfigManager.load_config()
  │     │     └─→ ~/.iso27001/config.yml
  │     │
  │     ├─→ Template Engine: TemplateEngine.render_policy()
  │     │     ├─→ Load template: templates/policies/*.md
  │     │     └─→ Render with Jinja2
  │     │
  │     └─→ Save output: output/policies/*.md
  │
  └─→ Display success message (Rich console)
```

### Risk Management Flow

```
User: iso27001 risks add --interactive
  │
  ├─→ CLI (risks.py)
  │     │
  │     ├─→ Prompt for input (Rich.Prompt)
  │     │     ├─→ Name, description, category
  │     │     ├─→ Assets affected
  │     │     ├─→ Impact (1-5), Likelihood (1-5)
  │     │     └─→ Treatment, mitigation measures
  │     │
  │     ├─→ Validate inputs (validators.py)
  │     │     ├─→ validate_risk_score(impact)
  │     │     ├─→ validate_risk_score(likelihood)
  │     │     └─→ validate_choice(treatment, [...])
  │     │
  │     ├─→ RiskManager.add_risk(data)
  │     │     ├─→ Generate ID: RISK-001
  │     │     ├─→ Calculate score: impact × likelihood
  │     │     ├─→ Determine level: high/medium/low/critical
  │     │     ├─→ Add to data['risks']
  │     │     └─→ Save to ~/.iso27001/data/risks.yml
  │     │
  │     └─→ Display confirmation
  │
  └─→ Risk added successfully ✓
```

### Audit Readiness Flow

```
User: iso27001 audit readiness
  │
  ├─→ CLI (audit.py)
  │     │
  │     ├─→ AuditHelper.assess_readiness()
  │     │     │
  │     │     ├─→ Load controls: ControlsTracker.load()
  │     │     │     └─→ ~/.iso27001/data/controls.yml
  │     │     │
  │     │     ├─→ Count implemented controls
  │     │     │     ├─→ status == 'implemented' OR 'verified'
  │     │     │     └─→ implemented / total × 100 = percentage
  │     │     │
  │     │     ├─→ Determine readiness level
  │     │     │     ├─→ ≥90%: Excellent
  │     │     │     ├─→ ≥75%: Good
  │     │     │     ├─→ ≥60%: Fair
  │     │     │     └─→ <60%: Poor
  │     │     │
  │     │     └─→ Return assessment dict
  │     │
  │     └─→ Display readiness report (Rich table)
  │           ├─→ Progress bar
  │           ├─→ Level (colored)
  │           ├─→ Recommendations
  │           └─→ Next steps
  │
  └─→ Assessment complete
```

---

## 🎨 Design Patterns

### 1. Template Method Pattern

**Class**: `YAMLStorage`

```python
class YAMLStorage:
    def load(self):
        # Common loading logic
        data = yaml.safe_load(content)
        return data if data else self._get_default_data()

    def _get_default_data(self):
        # Override in subclasses
        raise NotImplementedError
```

**Subclasses override `_get_default_data()`**:

```python
class ControlsTracker(YAMLStorage):
    def _get_default_data(self):
        return {
            'controls': {},
            'last_updated': None
        }

class RiskManager(YAMLStorage):
    def _get_default_data(self):
        return {
            'risks': [],
            'last_updated': None
        }
```

### 2. Repository Pattern

**Manager Classes** act as repositories:

```python
# Repository interface
class RiskManager:
    def get_risk(self, id: str) -> Optional[Dict]
    def get_all_risks(self) -> List[Dict]
    def add_risk(self, data: Dict) -> str
    def update_risk(self, id: str, updates: Dict) -> bool
    def delete_risk(self, id: str) -> bool
```

### 3. Strategy Pattern

**Validators** implement different validation strategies:

```python
def validate_email(email: str) -> str:
    # Email validation strategy
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError(...)

def validate_control_id(control_id: str) -> str:
    # Control ID validation strategy
    pattern = r'^A\.[5-8]\.\d{1,2}$'
    if not re.match(pattern, control_id):
        raise ValidationError(...)
```

### 4. Factory Pattern

**Risk ID Generation**:

```python
def _generate_risk_id(self) -> str:
    """Factory method for unique IDs"""
    existing_ids = [r['id'] for r in self.data['risks']]
    counter = 1

    while True:
        risk_id = f"RISK-{counter:03d}"
        if risk_id not in existing_ids:
            return risk_id
        counter += 1
```

### 5. Singleton Pattern (Implicit)

**Logger**:

```python
# logger.py
def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name)
    return logger

# Global instance
logger = get_logger()  # Singleton-like
```

---

## 🔌 Extension Points

### Adding a New Command Group

```python
# 1. Create commands/new_feature.py
import click
from rich.console import Console

console = Console()

@click.group()
def new_feature():
    """New feature description"""
    pass

@new_feature.command()
def subcommand():
    """Subcommand description"""
    console.print("Executing...")

# 2. Register in cli.py
from iso27001_toolkit.commands import new_feature

main.add_command(new_feature.new_feature)
```

### Adding a New Validator

```python
# validators.py
def validate_custom(value: str) -> str:
    """Validate custom format"""
    if not matches_custom_format(value):
        raise ValidationError(f"Invalid format: {value}")
    return value
```

### Adding a New Template

```jinja2
{# templates/policies/my_new_policy.md #}
# {{ organization_name }} - My New Policy

**Effective Date**: {{ effective_date }}

## 1. Purpose
{{ custom_section_1 }}

## 2. Scope
{{ custom_section_2 }}
```

---

## 📊 Performance Considerations

### Current Performance Characteristics

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Load risks | O(n) | YAML parsing |
| Add risk | O(n) | Generate unique ID |
| Search risk by ID | O(n) | Linear search |
| Generate report | O(n) | Template rendering |
| Load controls | O(1) | Static data (cached) |

### Optimization Opportunities

1. **Caching**: Cache `controls_data.py` (loaded multiple times)
2. **Indexing**: Add ID→index mapping for O(1) lookups
3. **Lazy Loading**: Load templates on-demand
4. **Batch Operations**: Support bulk risk imports

**Example Cache**:

```python
# controls_data.py
_CONTROLS_CACHE = None

def get_all_controls() -> List[Dict]:
    global _CONTROLS_CACHE
    if _CONTROLS_CACHE is None:
        _CONTROLS_CACHE = _load_controls()
    return _CONTROLS_CACHE
```

---

## 🧪 Testing Strategy

### Test Layers

```
┌─────────────────────────────────┐
│   E2E / Integration Tests       │  ← Full workflows
├─────────────────────────────────┤
│   Component Tests               │  ← Managers, Trackers
├─────────────────────────────────┤
│   Unit Tests                    │  ← Validators, Utils
└─────────────────────────────────┘
```

### Test Fixtures (`conftest.py`)

```python
@pytest.fixture
def temp_dir():
    """Temporary directory for test isolation"""

@pytest.fixture
def mock_config_dir(temp_dir):
    """Mock ~/.iso27001/ directory"""

@pytest.fixture
def sample_risk_data():
    """Sample risk for testing"""

@pytest.fixture
def encryption_key_file(temp_dir):
    """Test encryption key"""
```

---

## 🚀 Deployment Architecture

### Standalone Installation

```
User Machine
├── Python 3.8+ environment
├── pip install iso27001-toolkit
└── ~/.iso27001/ (created on first run)
    ├── config.yml
    ├── data/
    ├── logs/
    └── encryption.key
```

### Docker Deployment (Future)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install .

VOLUME /root/.iso27001

ENTRYPOINT ["iso27001"]
CMD ["--help"]
```

---

## 📚 Further Reading

- [Click Documentation](https://click.palletsprojects.com/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [Cryptography Library](https://cryptography.io/)
- [ISO 27001:2022 Standard](https://www.iso.org/standard/27001)
- [YAML Specification](https://yaml.org/)
- [Python Type Hints (PEP 484)](https://peps.python.org/pep-0484/)

---

**Maintainers**: ISO 27001 Toolkit Contributors
**License**: MIT
**Last Updated**: 2025-11-18
