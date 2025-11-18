# Guide Développeur API - ISO 27001 Toolkit

> Documentation complète de l'API Python pour les développeurs souhaitant intégrer ou étendre le toolkit

**Version**: 0.1.0  
**Python**: 3.8+  
**Dernière mise à jour**: 2025-11-18

---

## 📋 Table des matières

- [Introduction](#introduction)
- [Installation](#installation)
- [Architecture de l'API](#architecture-de-lapi)
- [Modules principaux](#modules-principaux)
- [Exemples d'utilisation](#exemples-dutilisation)
- [Création d'extensions](#création-dextensions)
- [Tests](#tests)
- [Best practices](#best-practices)

---

## Introduction

ISO 27001 Toolkit expose une API Python complète permettant de :
- **Intégrer** le toolkit dans vos applications
- **Automatiser** la gestion ISO 27001
- **Étendre** les fonctionnalités avec des plugins
- **Créer** des rapports personnalisés

---

## Installation

### Installation basique

```bash
pip install iso27001-toolkit
```

### Installation développeur

```bash
git clone https://github.com/GitCroque/iso27001-toolbox.git
cd iso27001-toolbox
pip install -e ".[dev]"
```

### Vérification

```python
import iso27001_toolkit
print(iso27001_toolkit.__version__)  # 0.1.0
```

---

## Architecture de l'API

### Structure des modules

```
iso27001_toolkit/
├── utils/
│   ├── risk_manager.py        # RiskManager class
│   ├── controls_tracker.py    # ControlsTracker class
│   ├── audit_helper.py         # AuditHelper class
│   ├── audit_trail.py          # AuditTrail class
│   ├── template_engine.py      # TemplateEngine class
│   ├── encryption.py           # Encryption utilities
│   ├── pdf_exporter.py         # PDFExporter class
│   ├── config.py               # Configuration
│   └── validators.py           # Validation functions
├── commands/                    # CLI commands (Click)
└── templates/                   # Jinja2 templates
```

---

## Modules principaux

### 1. RiskManager

**Localisation** : `iso27001_toolkit.utils.risk_manager`

#### Classe `RiskManager`

**Description** : Gestionnaire du registre des risques ISO 27001.

**Méthodes publiques** :

```python
class RiskManager:
    """Risk register manager for ISO 27001"""

    def __init__(self, file_path: Optional[Path] = None):
        """
        Initialize Risk Manager.

        Args:
            file_path: Custom path to risks.yml (default: ~/.iso27001/data/risks.yml)
        """

    def add_risk(self,
                 title: str,
                 description: str,
                 probability: int,
                 impact: int,
                 category: str,
                 treatment: Optional[str] = None,
                 controls: Optional[List[str]] = None) -> str:
        """
        Add a new risk to the register.

        Args:
            title: Risk title
            description: Detailed description
            probability: Probability (1-5)
            impact: Impact (1-5)
            category: Category (confidentiality, integrity, availability, compliance, operational)
            treatment: Treatment strategy (mitigate, accept, transfer, avoid)
            controls: List of associated control IDs (e.g., ["A.5.15", "A.8.2"])

        Returns:
            str: Generated risk ID (e.g., "RISK-001")

        Raises:
            ValidationError: If validation fails
            IOError: If unable to write to file

        Example:
            >>> manager = RiskManager()
            >>> risk_id = manager.add_risk(
            ...     title="Data loss",
            ...     description="Server failure without backup",
            ...     probability=3,
            ...     impact=5,
            ...     category="availability"
            ... )
            >>> print(risk_id)
            RISK-001
        """

    def get_risk(self, risk_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a risk by ID.

        Args:
            risk_id: Risk ID (e.g., "RISK-001")

        Returns:
            Dict containing risk data, or None if not found

        Example:
            >>> manager = RiskManager()
            >>> risk = manager.get_risk("RISK-001")
            >>> print(risk['title'])
            Data loss
        """

    def get_all_risks(self) -> List[Dict[str, Any]]:
        """
        Get all risks.

        Returns:
            List of risk dictionaries

        Example:
            >>> manager = RiskManager()
            >>> risks = manager.get_all_risks()
            >>> len(risks)
            15
        """

    def update_risk(self,
                    risk_id: str,
                    updates: Dict[str, Any]) -> bool:
        """
        Update an existing risk.

        Args:
            risk_id: Risk ID
            updates: Dictionary of fields to update

        Returns:
            True if updated, False if risk not found

        Example:
            >>> manager = RiskManager()
            >>> manager.update_risk("RISK-001", {
            ...     "probability": 2,
            ...     "treatment": "mitigated"
            ... })
            True
        """

    def delete_risk(self, risk_id: str) -> bool:
        """
        Delete a risk.

        Args:
            risk_id: Risk ID

        Returns:
            True if deleted, False if not found
        """

    def calculate_risk_score(self,
                            probability: int,
                            impact: int) -> Tuple[int, str]:
        """
        Calculate risk score and level.

        Args:
            probability: 1-5
            impact: 1-5

        Returns:
            Tuple of (score, level)
            - score: 1-25
            - level: "critical" | "high" | "medium" | "low"

        Example:
            >>> manager = RiskManager()
            >>> score, level = manager.calculate_risk_score(5, 5)
            >>> print(f"{score} - {level}")
            25 - critical
        """

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get risk statistics.

        Returns:
            Dictionary with:
            - total: Total number of risks
            - by_level: Count by level (critical, high, medium, low)
            - by_category: Count by category
            - by_treatment: Count by treatment strategy

        Example:
            >>> manager = RiskManager()
            >>> stats = manager.get_statistics()
            >>> print(stats['by_level'])
            {'critical': 2, 'high': 5, 'medium': 7, 'low': 3}
        """

    def generate_risk_matrix(self) -> str:
        """
        Generate a 5x5 risk matrix (text representation).

        Returns:
            String with ASCII art matrix

        Example:
            >>> manager = RiskManager()
            >>> matrix = manager.generate_risk_matrix()
            >>> print(matrix)
                      Impact →
                1    2    3    4    5
              ┌────┬────┬────┬────┬────┐
            5 │    │ 1  │    │ 2  │ 3  │
            4 │    │    │ 1  │    │ 1  │
            3 │    │    │ 2  │ 1  │    │
            2 │ 1  │    │    │    │    │
            1 │    │    │    │    │    │
              └────┴────┴────┴────┴────┘
        """
```

**Exemple complet** :

```python
from iso27001_toolkit.utils.risk_manager import RiskManager

# Initialiser
manager = RiskManager()

# Ajouter un risque
risk_id = manager.add_risk(
    title="Ransomware infection",
    description="Malware could encrypt company data",
    probability=4,
    impact=5,
    category="availability",
    treatment="mitigate",
    controls=["A.8.7", "A.8.8", "A.8.23"]
)

print(f"Created risk: {risk_id}")

# Récupérer
risk = manager.get_risk(risk_id)
print(f"Risk score: {risk['score']}/25 ({risk['level']})")

# Mettre à jour
manager.update_risk(risk_id, {
    "probability": 2,  # Reduced after mitigation
    "notes": "Antivirus deployed, backups configured"
})

# Statistiques
stats = manager.get_statistics()
print(f"Total risks: {stats['total']}")
print(f"Critical: {stats['by_level']['critical']}")
```

---

### 2. ControlsTracker

**Localisation** : `iso27001_toolkit.utils.controls_tracker`

#### Classe `ControlsTracker`

**Description** : Suivi des 114 contrôles ISO 27001:2022 (Annexe A).

**Pattern** : Singleton

**Méthodes publiques** :

```python
class ControlsTracker:
    """Tracker for 114 ISO 27001:2022 controls (Annex A)"""

    def __init__(self):
        """
        Initialize tracker.

        Note: This is a singleton. Use ControlsTracker() to get the instance.
        """

    def initialize(self) -> None:
        """
        Initialize tracker with 114 controls from iso27001_controls.yml.

        Creates ~/.iso27001/data/controls.yml if it doesn't exist.

        Example:
            >>> tracker = ControlsTracker()
            >>> tracker.initialize()
            >>> print("Tracker initialized")
        """

    def get_control(self, control_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a control by ID.

        Args:
            control_id: Control ID (e.g., "A.5.1", "A.8.23")

        Returns:
            Dict with control data or None

        Example:
            >>> tracker = ControlsTracker()
            >>> control = tracker.get_control("A.5.1")
            >>> print(control['title'])
            Policies for information security
        """

    def get_all_controls(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all 114 controls.

        Returns:
            Dict mapping control_id → control_data

        Example:
            >>> tracker = ControlsTracker()
            >>> controls = tracker.get_all_controls()
            >>> print(len(controls))
            114
        """

    def update_control_status(self,
                              control_id: str,
                              status: str,
                              notes: Optional[str] = None,
                              evidence: Optional[List[str]] = None,
                              priority: Optional[str] = None) -> bool:
        """
        Update control status and metadata.

        Args:
            control_id: Control ID
            status: Status ("not_started" | "in_progress" | "implemented" | "verified")
            notes: Implementation notes
            evidence: List of evidence files/URLs
            priority: Priority ("low" | "medium" | "high" | "critical")

        Returns:
            True if updated, False if control not found

        Raises:
            ValidationError: If status or priority invalid

        Example:
            >>> tracker = ControlsTracker()
            >>> tracker.update_control_status(
            ...     "A.5.1",
            ...     status="implemented",
            ...     notes="Security policy approved by CEO on 2024-01-15",
            ...     evidence=["policy_v1.0.pdf", "approval_email.pdf"],
            ...     priority="high"
            ... )
            True
        """

    def get_controls_by_status(self, status: str) -> List[Dict[str, Any]]:
        """
        Get all controls with a specific status.

        Args:
            status: Status to filter by

        Returns:
            List of controls

        Example:
            >>> tracker = ControlsTracker()
            >>> implemented = tracker.get_controls_by_status("implemented")
            >>> print(f"{len(implemented)} controls implemented")
            45 controls implemented
        """

    def get_controls_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get all controls in a category.

        Args:
            category: Category ("A.5" | "A.6" | "A.7" | "A.8")

        Returns:
            List of controls

        Example:
            >>> tracker = ControlsTracker()
            >>> org_controls = tracker.get_controls_by_category("A.5")
            >>> print(f"{len(org_controls)} organizational controls")
            37 organizational controls
        """

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get implementation statistics.

        Returns:
            Dict with:
            - total: 114
            - by_status: Count by status
            - by_category: Count by category (A.5, A.6, A.7, A.8)
            - by_priority: Count by priority
            - maturity_score: % implemented (0-100)

        Example:
            >>> tracker = ControlsTracker()
            >>> stats = tracker.get_statistics()
            >>> print(f"Maturity: {stats['maturity_score']}%")
            Maturity: 65.8%
        """

    def generate_soa(self) -> str:
        """
        Generate Statement of Applicability (Markdown).

        Returns:
            Markdown string with SOA

        Example:
            >>> tracker = ControlsTracker()
            >>> soa = tracker.generate_soa()
            >>> Path("soa.md").write_text(soa)
        """

    @classmethod
    def reset_instance(cls) -> None:
        """
        Reset singleton instance (for testing).

        Example:
            >>> ControlsTracker.reset_instance()
        """
```

**Exemple complet** :

```python
from iso27001_toolkit.utils.controls_tracker import ControlsTracker

# Obtenir l'instance (singleton)
tracker = ControlsTracker()

# Initialiser
tracker.initialize()

# Mettre à jour plusieurs contrôles
controls_to_implement = [
    ("A.5.1", "Policies for information security"),
    ("A.5.2", "Information security roles"),
    ("A.8.2", "Privileged access rights"),
]

for control_id, title in controls_to_implement:
    tracker.update_control_status(
        control_id,
        status="implemented",
        notes=f"{title} - Implemented on 2024-01-15",
        evidence=[f"{control_id}_evidence.pdf"],
        priority="high"
    )
    print(f"✓ {control_id} implemented")

# Statistiques
stats = tracker.get_statistics()
print(f"\nMaturity Score: {stats['maturity_score']:.1f}%")
print(f"Implemented: {stats['by_status']['implemented']}/114")

# Générer SOA
soa = tracker.generate_soa()
with open("soa.md", "w") as f:
    f.write(soa)
print("\n✓ SOA generated")
```

---

### 3. AuditHelper

**Localisation** : `iso27001_toolkit.utils.audit_helper`

#### Classe `AuditHelper`

**Description** : Assistant pour la préparation d'audits ISO 27001.

**Méthodes publiques** :

```python
class AuditHelper:
    """Helper for ISO 27001 audit preparation"""

    def __init__(self):
        """Initialize audit helper."""

    def assess_readiness(self) -> Dict[str, Any]:
        """
        Assess audit readiness.

        Returns:
            Dict with:
            - percentage: Readiness percentage (0-100)
            - level: "excellent" | "good" | "fair" | "poor"
            - implemented_controls: Number of implemented controls
            - total_controls: 114
            - critical_risks: Number of critical risks
            - recommendations: List of recommendations

        Example:
            >>> helper = AuditHelper()
            >>> assessment = helper.assess_readiness()
            >>> print(f"Readiness: {assessment['level']} ({assessment['percentage']}%)")
            Readiness: good (78.5%)
        """

    def generate_checklist(self) -> List[Dict[str, Any]]:
        """
        Generate audit checklist for all 114 controls.

        Returns:
            List of dicts with:
            - control_id: Control ID
            - title: Control title
            - questions: List of audit questions
            - evidence_required: List of required evidence

        Example:
            >>> helper = AuditHelper()
            >>> checklist = helper.generate_checklist()
            >>> for item in checklist[:3]:
            ...     print(f"{item['control_id']}: {item['title']}")
            A.5.1: Policies for information security
            A.5.2: Information security roles and responsibilities
            A.5.3: Segregation of duties
        """

    def generate_soa(self) -> str:
        """
        Generate Statement of Applicability.

        Returns:
            Markdown string with SOA

        Example:
            >>> helper = AuditHelper()
            >>> soa = helper.generate_soa()
            >>> Path("soa.md").write_text(soa)
        """

    def generate_risk_register(self) -> str:
        """
        Generate risk register report.

        Returns:
            Markdown string with formatted risk register

        Example:
            >>> helper = AuditHelper()
            >>> report = helper.generate_risk_register()
            >>> Path("risk_register.md").write_text(report)
        """

    def perform_gap_analysis(self) -> List[Dict[str, Any]]:
        """
        Perform gap analysis (identify non-implemented controls).

        Returns:
            List of gaps with:
            - control_id: Control ID
            - title: Control title
            - category: Category
            - priority: Priority level
            - recommendation: Implementation recommendation

        Example:
            >>> helper = AuditHelper()
            >>> gaps = helper.perform_gap_analysis()
            >>> print(f"{len(gaps)} gaps identified")
            35 gaps identified
            >>> for gap in gaps[:3]:
            ...     print(f"- {gap['control_id']}: {gap['title']}")
        """
```

**Exemple complet** :

```python
from iso27001_toolkit.utils.audit_helper import AuditHelper
from pathlib import Path

# Initialiser
helper = AuditHelper()

# 1. Évaluer la préparation
assessment = helper.assess_readiness()
print(f"Readiness Level: {assessment['level']}")
print(f"Score: {assessment['percentage']}%")
print(f"Controls: {assessment['implemented_controls']}/114")

# 2. Générer checklist
checklist = helper.generate_checklist()
print(f"\nGenerated checklist with {len(checklist)} items")

# 3. Gap analysis
gaps = helper.perform_gap_analysis()
print(f"\nGaps identified: {len(gaps)}")

# Afficher top 5 gaps prioritaires
high_priority_gaps = [g for g in gaps if g['priority'] == 'high'][:5]
print("\nTop 5 high-priority gaps:")
for gap in high_priority_gaps:
    print(f"  - {gap['control_id']}: {gap['title']}")
    print(f"    Recommendation: {gap['recommendation']}")

# 4. Générer rapports
soa = helper.generate_soa()
Path("soa.md").write_text(soa)

risk_register = helper.generate_risk_register()
Path("risk_register.md").write_text(risk_register)

print("\n✓ Reports generated")
```

---

### 4. AuditTrail

**Localisation** : `iso27001_toolkit.utils.audit_trail`

#### Classe `AuditTrail`

**Description** : Journal d'audit immuable (append-only).

**Pattern** : Singleton

**Méthodes publiques** :

```python
class AuditTrail:
    """Immutable audit trail for all ISO 27001 operations"""

    def __init__(self):
        """Initialize audit trail (singleton)."""

    def log(self,
            action: str,
            entity_type: str,
            entity_id: str,
            details: Optional[Dict[str, Any]] = None,
            status: str = "success") -> None:
        """
        Log an action to the audit trail.

        Args:
            action: Action performed (e.g., "control_status_updated")
            entity_type: Entity type ("control", "risk", "policy", etc.)
            entity_id: Entity identifier
            details: Additional details (dict)
            status: "success" | "failure"

        Example:
            >>> from iso27001_toolkit.utils.audit_trail import AuditTrail
            >>> trail = AuditTrail()
            >>> trail.log(
            ...     action="control_status_updated",
            ...     entity_type="control",
            ...     entity_id="A.5.1",
            ...     details={"old_status": "not_started", "new_status": "implemented"},
            ...     status="success"
            ... )
        """

    def get_entries(self,
                   limit: Optional[int] = None,
                   entity_type: Optional[str] = None,
                   action: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve audit trail entries.

        Args:
            limit: Maximum number of entries (most recent first)
            entity_type: Filter by entity type
            action: Filter by action

        Returns:
            List of audit entries

        Example:
            >>> trail = AuditTrail()
            >>> # Last 10 entries
            >>> recent = trail.get_entries(limit=10)
            >>>
            >>> # All control updates
            >>> control_updates = trail.get_entries(entity_type="control")
        """

    @classmethod
    def reset_instance(cls) -> None:
        """Reset singleton (for testing)."""
```

**Exemple complet** :

```python
from iso27001_toolkit.utils.audit_trail import AuditTrail
from datetime import datetime

# Obtenir l'instance
trail = AuditTrail()

# Logger différentes actions
trail.log(
    action="risk_created",
    entity_type="risk",
    entity_id="RISK-001",
    details={"title": "Data breach", "score": 20},
    status="success"
)

trail.log(
    action="policy_generated",
    entity_type="policy",
    entity_id="information_security_policy",
    details={"format": "markdown", "version": "1.0"},
    status="success"
)

trail.log(
    action="control_status_updated",
    entity_type="control",
    entity_id="A.5.1",
    details={"old": "not_started", "new": "implemented"},
    status="success"
)

# Récupérer entrées
all_entries = trail.get_entries()
print(f"Total entries: {len(all_entries)}")

# Récupérer les 10 dernières
recent = trail.get_entries(limit=10)
for entry in recent:
    print(f"{entry['timestamp']}: {entry['action']} on {entry['entity_id']}")

# Filtrer par type
risk_entries = trail.get_entries(entity_type="risk")
print(f"\nRisk operations: {len(risk_entries)}")
```

---

### 5. TemplateEngine

**Localisation** : `iso27001_toolkit.utils.template_engine`

#### Classe `TemplateEngine`

**Description** : Moteur de rendu de templates Jinja2.

**Méthodes publiques** :

```python
class TemplateEngine:
    """Jinja2 template rendering engine"""

    def __init__(self, template_dir: Optional[Path] = None):
        """
        Initialize template engine.

        Args:
            template_dir: Custom template directory (default: built-in templates)
        """

    def render_policy(self,
                     policy_name: str,
                     context: Dict[str, Any]) -> str:
        """
        Render a policy template.

        Args:
            policy_name: Policy template name (e.g., "information_security_policy")
            context: Template variables

        Returns:
            Rendered Markdown string

        Example:
            >>> engine = TemplateEngine()
            >>> context = {
            ...     "organization_name": "ACME Corp",
            ...     "ciso_name": "John Doe",
            ...     "ciso_email": "john.doe@acme.com",
            ...     "effective_date": "2024-01-01"
            ... }
            >>> policy = engine.render_policy("information_security_policy", context)
            >>> Path("policy.md").write_text(policy)
        """

    def list_available_policies(self) -> List[str]:
        """
        List all available policy templates.

        Returns:
            List of policy names

        Example:
            >>> engine = TemplateEngine()
            >>> policies = engine.list_available_policies()
            >>> for policy in policies:
            ...     print(policy)
            information_security_policy
            access_control_policy
            asset_management_policy
            ...
        """

    def render_custom_template(self,
                               template_file: Path,
                               context: Dict[str, Any]) -> str:
        """
        Render a custom template file.

        Args:
            template_file: Path to template file (.md, .yml, .html)
            context: Template variables

        Returns:
            Rendered content

        Example:
            >>> engine = TemplateEngine()
            >>> context = {"company": "ACME", "date": "2024-01-15"}
            >>> content = engine.render_custom_template(
            ...     Path("templates/custom_report.md"),
            ...     context
            ... )
        """
```

**Exemple complet** :

```python
from iso27001_toolkit.utils.template_engine import TemplateEngine
from iso27001_toolkit.utils.config import CONFIG_DIR
from pathlib import Path
import yaml

# Charger la configuration organisation
with open(CONFIG_DIR / "config.yml") as f:
    config = yaml.safe_load(f)

# Initialiser le moteur
engine = TemplateEngine()

# Contexte avec toutes les variables
context = {
    "organization_name": config.get("organization_name", "My Company"),
    "ciso_name": config.get("ciso_name", "CISO"),
    "ciso_email": config.get("ciso_email", "ciso@example.com"),
    "dpo_name": config.get("dpo_name", "DPO"),
    "dpo_email": config.get("dpo_email", "dpo@example.com"),
    "effective_date": config.get("effective_date", "2024-01-01"),
    "review_period": config.get("review_period", "Annual"),
    "current_date": "2024-11-18"
}

# Générer toutes les politiques
policies = engine.list_available_policies()
output_dir = Path("output/policies")
output_dir.mkdir(parents=True, exist_ok=True)

for policy_name in policies:
    content = engine.render_policy(policy_name, context)
    output_file = output_dir / f"{policy_name}.md"
    output_file.write_text(content)
    print(f"✓ Generated {policy_name}")

print(f"\n✓ {len(policies)} policies generated in {output_dir}")
```

---

### 6. PDFExporter

**Localisation** : `iso27001_toolkit.utils.pdf_exporter`

#### Classe `PDFExporter`

**Description** : Export PDF professionnel avec WeasyPrint.

**Méthodes publiques** :

```python
class PDFExporter:
    """Professional PDF exporter for ISO 27001 documents"""

    def __init__(self):
        """
        Initialize PDF exporter.

        Raises:
            ImportError: If WeasyPrint not installed
        """

    def markdown_to_pdf(self,
                       markdown_file: Path,
                       output_pdf: Path,
                       title: Optional[str] = None,
                       organization: str = "Organization",
                       document_type: str = "ISO 27001 Document",
                       add_cover: bool = True,
                       metadata: Optional[Dict[str, str]] = None) -> Path:
        """
        Convert Markdown to PDF.

        Args:
            markdown_file: Input Markdown file
            output_pdf: Output PDF file
            title: Document title (auto-detected if None)
            organization: Organization name
            document_type: Document type
            add_cover: Add professional cover page
            metadata: Additional metadata for cover

        Returns:
            Path to generated PDF

        Example:
            >>> exporter = PDFExporter()
            >>> exporter.markdown_to_pdf(
            ...     markdown_file=Path("soa.md"),
            ...     output_pdf=Path("soa.pdf"),
            ...     organization="ACME Corp",
            ...     document_type="Statement of Applicability"
            ... )
            PosixPath('soa.pdf')
        """

    def export_policy_pdf(self,
                         policy_file: Path,
                         output_pdf: Path,
                         organization: str = "Organization") -> Path:
        """Export a policy to PDF."""

    def export_soa_pdf(self,
                      soa_file: Path,
                      output_pdf: Path,
                      organization: str = "Organization",
                      maturity_score: Optional[float] = None) -> Path:
        """Export Statement of Applicability to PDF."""

    def export_risk_register_pdf(self,
                                 risk_file: Path,
                                 output_pdf: Path,
                                 organization: str = "Organization",
                                 total_risks: Optional[int] = None) -> Path:
        """Export risk register to PDF."""
```

**Exemple complet** :

```python
from iso27001_toolkit.utils.pdf_exporter import get_pdf_exporter, check_pdf_support
from iso27001_toolkit.utils.audit_helper import AuditHelper
from pathlib import Path

# Vérifier support PDF
if not check_pdf_support():
    print("WeasyPrint not installed. Run: pip install iso27001-toolkit[pdf]")
    exit(1)

# Initialiser
exporter = get_pdf_exporter()
helper = AuditHelper()

# Générer SOA en Markdown
soa_md = helper.generate_soa()
soa_file = Path("soa.md")
soa_file.write_text(soa_md)

# Convertir en PDF
pdf_file = exporter.export_soa_pdf(
    soa_file=soa_file,
    output_pdf=Path("soa.pdf"),
    organization="ACME Corporation",
    maturity_score=75.5
)

print(f"✓ PDF generated: {pdf_file}")
print(f"  Size: {pdf_file.stat().st_size / 1024:.1f} KB")

# Nettoyer Markdown temporaire
soa_file.unlink()
```

---

### 7. Validators

**Localisation** : `iso27001_toolkit.utils.validators`

**Description** : Fonctions de validation et sanitization.

**Fonctions disponibles** :

```python
def validate_email(email: str) -> str:
    """
    Validate email address format.

    Args:
        email: Email to validate

    Returns:
        Validated email

    Raises:
        ValidationError: If invalid

    Example:
        >>> validate_email("john.doe@example.com")
        'john.doe@example.com'
        >>> validate_email("invalid")
        ValidationError: Invalid email format
    """

def validate_control_id(control_id: str) -> str:
    """
    Validate ISO 27001:2022 control ID.

    Args:
        control_id: Control ID (e.g., "A.5.1")

    Returns:
        Validated control ID

    Raises:
        ValidationError: If invalid format

    Example:
        >>> validate_control_id("A.5.1")
        'A.5.1'
        >>> validate_control_id("B.1.1")
        ValidationError: Invalid control ID
    """

def validate_risk_score(value: Any, min_val: int = 1, max_val: int = 5) -> int:
    """
    Validate risk score (probability or impact).

    Args:
        value: Score to validate
        min_val: Minimum value (default 1)
        max_val: Maximum value (default 5)

    Returns:
        Validated integer

    Example:
        >>> validate_risk_score(4)
        4
        >>> validate_risk_score(10)
        ValidationError: Score must be between 1 and 5
    """

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal.

    Args:
        filename: Filename to sanitize

    Returns:
        Sanitized filename

    Example:
        >>> sanitize_filename("report_2024.pdf")
        'report_2024.pdf'
        >>> sanitize_filename("../../../etc/passwd")
        '___etc_passwd'
    """
```

**Exemple complet** :

```python
from iso27001_toolkit.utils.validators import (
    validate_email,
    validate_control_id,
    validate_risk_score,
    sanitize_filename,
    ValidationError
)

# Validation d'email
try:
    email = validate_email("ciso@acme.com")
    print(f"✓ Valid email: {email}")
except ValidationError as e:
    print(f"✗ Invalid: {e}")

# Validation de control ID
try:
    control_id = validate_control_id("A.8.23")
    print(f"✓ Valid control: {control_id}")
except ValidationError as e:
    print(f"✗ Invalid: {e}")

# Validation de score
try:
    impact = validate_risk_score(5, min_val=1, max_val=5)
    probability = validate_risk_score(3, min_val=1, max_val=5)
    print(f"✓ Risk score: {impact} × {probability} = {impact * probability}")
except ValidationError as e:
    print(f"✗ Invalid score: {e}")

# Sanitization de filename
unsafe_filename = "../../etc/passwd"
safe_filename = sanitize_filename(unsafe_filename)
print(f"Sanitized: '{unsafe_filename}' → '{safe_filename}'")
```

---

## Exemples d'utilisation

### Exemple 1 : Application Flask avec ISO 27001 Toolkit

```python
from flask import Flask, jsonify, request
from iso27001_toolkit.utils.risk_manager import RiskManager
from iso27001_toolkit.utils.controls_tracker import ControlsTracker

app = Flask(__name__)
risk_manager = RiskManager()
controls_tracker = ControlsTracker()

@app.route('/api/risks', methods=['GET'])
def get_risks():
    """Get all risks"""
    risks = risk_manager.get_all_risks()
    return jsonify(risks)

@app.route('/api/risks', methods=['POST'])
def create_risk():
    """Create a new risk"""
    data = request.json
    risk_id = risk_manager.add_risk(
        title=data['title'],
        description=data['description'],
        probability=data['probability'],
        impact=data['impact'],
        category=data['category']
    )
    return jsonify({"risk_id": risk_id}), 201

@app.route('/api/controls/stats', methods=['GET'])
def get_control_stats():
    """Get control implementation statistics"""
    stats = controls_tracker.get_statistics()
    return jsonify(stats)

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    """Get dashboard data"""
    return jsonify({
        "risks": risk_manager.get_statistics(),
        "controls": controls_tracker.get_statistics()
    })

if __name__ == '__main__':
    controls_tracker.initialize()
    app.run(debug=True)
```

### Exemple 2 : Script d'automatisation quotidien

```python
#!/usr/bin/env python3
"""Daily ISO 27001 automation script"""

from iso27001_toolkit.utils.risk_manager import RiskManager
from iso27001_toolkit.utils.controls_tracker import ControlsTracker
from iso27001_toolkit.utils.audit_helper import AuditHelper
from iso27001_toolkit.utils.audit_trail import AuditTrail
from datetime import datetime
from pathlib import Path
import smtplib
from email.message import EmailMessage

def daily_iso27001_check():
    """Perform daily ISO 27001 health check"""

    print(f"📊 ISO 27001 Daily Check - {datetime.now().strftime('%Y-%m-%d')}")
    print("=" * 60)

    # Initialize
    risk_mgr = RiskManager()
    controls = ControlsTracker()
    audit = AuditHelper()
    trail = AuditTrail()

    # 1. Check critical risks
    risk_stats = risk_mgr.get_statistics()
    critical_count = risk_stats['by_level'].get('critical', 0)

    print(f"\n1. Risk Status:")
    print(f"   Total: {risk_stats['total']}")
    print(f"   Critical: {critical_count}")

    if critical_count > 5:
        alert = f"⚠️  HIGH ALERT: {critical_count} critical risks!"
        print(f"   {alert}")
        send_alert_email(alert)

    # 2. Check control implementation
    control_stats = controls.get_statistics()
    maturity = control_stats['maturity_score']

    print(f"\n2. Control Status:")
    print(f"   Maturity: {maturity:.1f}%")
    print(f"   Implemented: {control_stats['by_status'].get('implemented', 0)}/114")

    # 3. Assess readiness
    readiness = audit.assess_readiness()

    print(f"\n3. Audit Readiness:")
    print(f"   Level: {readiness['level']}")
    print(f"   Score: {readiness['percentage']:.1f}%")

    # 4. Recent audit trail
    recent_entries = trail.get_entries(limit=5)

    print(f"\n4. Recent Activity:")
    for entry in recent_entries:
        print(f"   - {entry['timestamp']}: {entry['action']}")

    # 5. Generate daily report
    report_dir = Path("reports/daily")
    report_dir.mkdir(parents=True, exist_ok=True)

    report_file = report_dir / f"daily_report_{datetime.now().strftime('%Y%m%d')}.md"

    with open(report_file, 'w') as f:
        f.write(f"# Daily ISO 27001 Report\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write(f"## Summary\n\n")
        f.write(f"- **Maturity**: {maturity:.1f}%\n")
        f.write(f"- **Critical Risks**: {critical_count}\n")
        f.write(f"- **Audit Readiness**: {readiness['level']} ({readiness['percentage']:.1f}%)\n")

    print(f"\n✓ Report saved: {report_file}")

def send_alert_email(alert_message: str):
    """Send alert email to CISO"""
    msg = EmailMessage()
    msg['Subject'] = f"ISO 27001 Alert - {datetime.now().strftime('%Y-%m-%d')}"
    msg['From'] = "iso27001-bot@example.com"
    msg['To'] = "ciso@example.com"
    msg.set_content(alert_message)

    # Send email (configure SMTP server)
    # with smtplib.SMTP('smtp.example.com', 587) as smtp:
    #     smtp.send_message(msg)

    print("   📧 Alert email sent")

if __name__ == '__main__':
    daily_iso27001_check()
```

---

## Création d'extensions

### Plugin personnalisé

**Exemple : Plugin de notification Slack**

```python
"""Slack notification plugin for ISO 27001 Toolkit"""

from iso27001_toolkit.utils.audit_trail import AuditTrail
import requests

class SlackNotifier:
    """Send notifications to Slack on important events"""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.trail = AuditTrail()

    def notify_critical_risk(self, risk_id: str, title: str, score: int):
        """Notify when a critical risk is created"""
        message = {
            "text": f"🚨 Critical Risk Created",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{risk_id}*: {title}\n*Score*: {score}/25"
                    }
                }
            ]
        }
        self._send(message)

    def notify_control_implemented(self, control_id: str, title: str):
        """Notify when a control is implemented"""
        message = {
            "text": f"✅ Control Implemented: {control_id}",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{control_id}*: {title}"
                    }
                }
            ]
        }
        self._send(message)

    def _send(self, message: dict):
        """Send message to Slack"""
        response = requests.post(self.webhook_url, json=message)
        if response.status_code != 200:
            print(f"Failed to send Slack notification: {response.text}")

# Usage
if __name__ == '__main__':
    from iso27001_toolkit.utils.risk_manager import RiskManager

    notifier = SlackNotifier(webhook_url="https://hooks.slack.com/...")
    risk_mgr = RiskManager()

    # Hook into risk creation
    def add_risk_with_notification(*args, **kwargs):
        risk_id = risk_mgr.add_risk(*args, **kwargs)
        risk = risk_mgr.get_risk(risk_id)

        if risk['level'] == 'critical':
            notifier.notify_critical_risk(
                risk_id=risk_id,
                title=risk['title'],
                score=risk['score']
            )

        return risk_id

    # Use the wrapped function
    add_risk_with_notification(
        title="Data breach",
        description="Potential data breach via SQL injection",
        probability=5,
        impact=5,
        category="confidentiality"
    )
```

---

## Tests

### Écrire des tests pour vos extensions

```python
import pytest
from iso27001_toolkit.utils.risk_manager import RiskManager
from iso27001_toolkit.utils.validators import ValidationError

class TestCustomRiskFunctions:
    """Test suite for custom risk functions"""

    def test_add_risk_with_controls(self, temp_dir, monkeypatch):
        """Test adding risk with associated controls"""
        # Setup
        from iso27001_toolkit.utils import config
        monkeypatch.setattr(config, 'CONFIG_DIR', temp_dir)

        manager = RiskManager()

        # Act
        risk_id = manager.add_risk(
            title="Test risk",
            description="Test",
            probability=3,
            impact=4,
            category="confidentiality",
            controls=["A.5.15", "A.8.2"]
        )

        # Assert
        risk = manager.get_risk(risk_id)
        assert risk is not None
        assert risk['controls'] == ["A.5.15", "A.8.2"]

    def test_invalid_probability_raises_error(self):
        """Test that invalid probability raises ValidationError"""
        manager = RiskManager()

        with pytest.raises(ValidationError):
            manager.add_risk(
                title="Test",
                description="Test",
                probability=10,  # Invalid (max 5)
                impact=3,
                category="availability"
            )
```

---

## Best Practices

### 1. Gestion des erreurs

```python
from iso27001_toolkit.utils.risk_manager import RiskManager
from iso27001_toolkit.utils.validators import ValidationError
import logging

logger = logging.getLogger(__name__)

def safe_add_risk(**kwargs):
    """Safely add a risk with error handling"""
    try:
        manager = RiskManager()
        risk_id = manager.add_risk(**kwargs)
        logger.info(f"Risk created: {risk_id}")
        return risk_id

    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return None

    except IOError as e:
        logger.error(f"File I/O error: {e}")
        return None

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return None
```

### 2. Configuration centralisée

```python
from pathlib import Path
import yaml

class ISO27001Config:
    """Centralized configuration"""

    def __init__(self, config_file: Path):
        with open(config_file) as f:
            self.config = yaml.safe_load(f)

    @property
    def organization_name(self) -> str:
        return self.config.get('organization_name', 'Organization')

    @property
    def ciso_email(self) -> str:
        return self.config.get('ciso_email', 'ciso@example.com')

# Usage
config = ISO27001Config(Path.home() / ".iso27001/config.yml")
print(config.organization_name)
```

### 3. Logging approprié

```python
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Path.home() / ".iso27001/logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('my_iso27001_app')

# Usage
logger.info("Starting ISO 27001 operations")
logger.warning("Critical risk detected")
logger.error("Failed to update control", exc_info=True)
```

---

## Ressources

- **Code source** : https://github.com/GitCroque/iso27001-toolbox
- **Documentation** : https://github.com/GitCroque/iso27001-toolbox/blob/main/README.md
- **Issues** : https://github.com/GitCroque/iso27001-toolbox/issues
- **Architecture** : [ARCHITECTURE.md](../../ARCHITECTURE.md)

---

**Dernière mise à jour** : 2025-11-18  
**Version** : 1.0.0
