"""Tests pour le gestionnaire de risques"""

import pytest
import tempfile
from pathlib import Path
from iso27001_toolkit.utils.risk_manager import RiskManager
from iso27001_toolkit.utils import config


@pytest.fixture
def temp_config_dir(monkeypatch):
    """Crée un répertoire temporaire pour les tests"""
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setattr(config, 'CONFIG_DIR', Path(tmpdir))
        yield Path(tmpdir)


@pytest.fixture
def manager(temp_config_dir):
    """Crée un gestionnaire de risques pour les tests"""
    return RiskManager()


def test_manager_initialization(manager):
    """Test l'initialisation du gestionnaire"""
    manager.initialize()
    assert 'risks' in manager.data
    assert isinstance(manager.data['risks'], list)


def test_add_risk(manager):
    """Test l'ajout d'un risque"""
    manager.initialize()

    risk_data = {
        'name': 'Test Risk',
        'description': 'Test description',
        'category': 'confidentiality',
        'assets': ['Asset 1'],
        'impact': 4,
        'likelihood': 3,
        'treatment': 'mitigate',
        'mitigation_measures': ['Measure 1']
    }

    risk_id = manager.add_risk(risk_data)
    assert risk_id.startswith('RISK-')

    risk = manager.get_risk(risk_id)
    assert risk is not None
    assert risk['name'] == 'Test Risk'
    assert risk['risk_score'] == 12  # 4 * 3
    assert risk['risk_level'] == 'high'


def test_risk_score_calculation(manager):
    """Test le calcul du score de risque"""
    # Risque faible
    score, level = manager._calculate_risk_score(2, 2)
    assert score == 4
    assert level == 'low'

    # Risque moyen
    score, level = manager._calculate_risk_score(3, 2)
    assert score == 6
    assert level == 'medium'

    # Risque élevé
    score, level = manager._calculate_risk_score(4, 3)
    assert score == 12
    assert level == 'high'

    # Risque critique
    score, level = manager._calculate_risk_score(5, 5)
    assert score == 25
    assert level == 'critical'


def test_update_risk(manager):
    """Test la mise à jour d'un risque"""
    manager.initialize()

    risk_data = {
        'name': 'Test Risk',
        'impact': 3,
        'likelihood': 3
    }

    risk_id = manager.add_risk(risk_data)

    # Mettre à jour
    updates = {
        'status': 'treated',
        'impact': 5,
        'likelihood': 4
    }

    success = manager.update_risk(risk_id, updates)
    assert success

    risk = manager.get_risk(risk_id)
    assert risk['status'] == 'treated'
    assert risk['risk_score'] == 20  # 5 * 4
    assert risk['risk_level'] == 'critical'


def test_get_risks_by_level(manager):
    """Test le filtrage par niveau"""
    manager.initialize()

    # Ajouter des risques de différents niveaux
    manager.add_risk({'name': 'Low', 'impact': 1, 'likelihood': 2})
    manager.add_risk({'name': 'High', 'impact': 4, 'likelihood': 3})
    manager.add_risk({'name': 'Critical', 'impact': 5, 'likelihood': 5})

    high_risks = manager.get_risks_by_level('high')
    assert len(high_risks) >= 1

    critical_risks = manager.get_risks_by_level('critical')
    assert len(critical_risks) >= 1


def test_delete_risk(manager):
    """Test la suppression d'un risque"""
    manager.initialize()

    risk_id = manager.add_risk({'name': 'To Delete'})
    assert manager.get_risk(risk_id) is not None

    success = manager.delete_risk(risk_id)
    assert success
    assert manager.get_risk(risk_id) is None


def test_get_statistics(manager):
    """Test les statistiques"""
    manager.initialize()

    manager.add_risk({'name': 'R1', 'impact': 2, 'likelihood': 2})
    manager.add_risk({'name': 'R2', 'impact': 4, 'likelihood': 3})
    manager.add_risk({'name': 'R3', 'impact': 5, 'likelihood': 5})

    stats = manager.get_statistics()
    assert stats['total'] >= 3
    assert 'by_level' in stats
    assert 'by_status' in stats
    assert 'by_treatment' in stats
