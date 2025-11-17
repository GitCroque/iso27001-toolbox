"""
Configuration commune pour les tests pytest
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import MagicMock


@pytest.fixture
def temp_dir():
    """Crée un répertoire temporaire pour les tests"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_config_dir(temp_dir, monkeypatch):
    """Mock le répertoire de configuration"""
    config_dir = temp_dir / ".iso27001"
    config_dir.mkdir(parents=True, exist_ok=True)

    # Patcher les chemins de configuration
    import iso27001_toolkit.utils.config as config_module
    monkeypatch.setattr(config_module, 'CONFIG_DIR', config_dir)
    monkeypatch.setattr(config_module, 'CONFIG_FILE', config_dir / 'config.yml')

    yield config_dir


@pytest.fixture
def mock_data_dir(mock_config_dir):
    """Mock le répertoire de données"""
    data_dir = mock_config_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


@pytest.fixture
def sample_organization_config():
    """Configuration d'organisation pour les tests"""
    return {
        'organization_name': 'Test Organization',
        'ciso_name': 'John Doe',
        'ciso_email': 'john.doe@test.com',
        'industry': 'Technology',
        'employee_count': '50',
        'certification_scope': 'IT Infrastructure',
    }


@pytest.fixture
def sample_risk_data():
    """Données de risque pour les tests"""
    return {
        'name': 'Test Risk',
        'description': 'A test risk description',
        'category': 'confidentiality',
        'assets': ['Server', 'Database'],
        'impact': 4,
        'likelihood': 3,
        'treatment': 'mitigate',
        'mitigation_measures': ['Implement firewall', 'Regular backups'],
        'owner': 'Security Team'
    }


@pytest.fixture
def sample_control_data():
    """Données de contrôle pour les tests"""
    return {
        'id': 'A.5.1',
        'name': 'Politiques de sécurité de l\'information',
        'category': 'A.5',
        'category_name': 'Contrôles organisationnels',
        'description': 'Des politiques de sécurité de l\'information doivent être définies',
        'objective': 'Fournir une orientation et un soutien de la direction',
    }


@pytest.fixture
def mock_console(monkeypatch):
    """Mock Rich console pour les tests CLI"""
    mock = MagicMock()
    import iso27001_toolkit.commands.risks as risks_module
    import iso27001_toolkit.commands.controls as controls_module
    import iso27001_toolkit.commands.policies as policies_module
    import iso27001_toolkit.commands.audit as audit_module

    monkeypatch.setattr(risks_module, 'console', mock)
    monkeypatch.setattr(controls_module, 'console', mock)
    monkeypatch.setattr(policies_module, 'console', mock)
    monkeypatch.setattr(audit_module, 'console', mock)

    return mock


@pytest.fixture
def encryption_key_file(temp_dir):
    """Crée un fichier de clé de chiffrement temporaire"""
    key_file = temp_dir / "test_encryption.key"
    return key_file
