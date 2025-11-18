"""Tests pour le tracker de contrôles"""

import pytest
import tempfile
import yaml
from pathlib import Path
from iso27001_toolkit.utils.controls_tracker import ControlsTracker
from iso27001_toolkit.utils import config


@pytest.fixture
def temp_config_dir(monkeypatch):
    """Crée un répertoire temporaire pour les tests"""
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setattr(config, 'CONFIG_DIR', Path(tmpdir))
        yield Path(tmpdir)


@pytest.fixture
def tracker(temp_config_dir):
    """Crée un tracker pour les tests"""
    return ControlsTracker()


def test_tracker_initialization(tracker):
    """Test l'initialisation du tracker"""
    tracker.initialize()
    assert 'controls' in tracker.data
    assert len(tracker.data['controls']) > 0


def test_update_control_status(tracker):
    """Test la mise à jour du statut d'un contrôle"""
    tracker.initialize()
    tracker.update_control_status('A.5.1', 'implemented')
    assert tracker.get_control_status('A.5.1') == 'implemented'


def test_update_control_priority(tracker):
    """Test la mise à jour de la priorité"""
    tracker.initialize()
    tracker.update_control_priority('A.5.1', 'high')
    assert tracker.get_control_priority('A.5.1') == 'high'


def test_add_control_evidence(tracker):
    """Test l'ajout de preuves"""
    tracker.initialize()
    evidence = ['Preuve 1', 'Preuve 2']
    tracker.add_control_evidence('A.5.1', evidence)
    assert len(tracker.get_control_evidence('A.5.1')) >= 2


def test_get_statistics(tracker):
    """Test les statistiques"""
    tracker.initialize()
    tracker.update_control_status('A.5.1', 'implemented')
    tracker.update_control_status('A.5.2', 'in_progress')

    stats = tracker.get_statistics()
    assert stats['total'] > 0
    assert stats['implemented'] >= 1
    assert stats['in_progress'] >= 1


def test_persistence(tracker, temp_config_dir):
    """Test la persistance des données"""
    tracker.initialize()
    tracker.update_control_status('A.5.1', 'verified')
    tracker.save()

    # Créer un nouveau tracker et vérifier les données
    new_tracker = ControlsTracker()
    assert new_tracker.get_control_status('A.5.1') == 'verified'
