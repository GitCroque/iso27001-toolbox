"""
Tests pour le module ControlsTracker
"""

import pytest
from pathlib import Path
from datetime import datetime

from iso27001_toolkit.utils.controls_tracker import ControlsTracker
from iso27001_toolkit.utils.controls_data import get_all_controls


class TestControlsTrackerInitialization:
    """Tests d'initialisation du ControlsTracker"""

    def test_init_creates_empty_tracker(self, mock_config_dir):
        """Test que l'initialisation crée un tracker vide"""
        tracker = ControlsTracker()
        assert tracker.data['controls'] == {}
        assert tracker.data['last_updated'] is None

    def test_initialize_creates_all_controls(self, mock_config_dir):
        """Test que initialize() crée tous les 114 contrôles"""
        tracker = ControlsTracker()
        tracker.initialize()

        all_controls = get_all_controls()
        assert len(tracker.data['controls']) == len(all_controls)

        # Vérifier que tous les contrôles sont présents
        for control in all_controls:
            assert control['id'] in tracker.data['controls']

    def test_initialize_sets_default_values(self, mock_config_dir):
        """Test que initialize() définit les valeurs par défaut"""
        tracker = ControlsTracker()
        tracker.initialize()

        # Vérifier le premier contrôle
        control_data = tracker.data['controls']['A.5.1']

        assert control_data['status'] == 'not_started'
        assert control_data['priority'] == 'medium'
        assert control_data['notes'] == ''
        assert control_data['evidence'] == []
        assert control_data['responsible_party'] == ''
        assert control_data['implementation_date'] is None
        assert control_data['review_date'] is None

    def test_initialize_preserves_existing_data(self, mock_config_dir):
        """Test que initialize() ne réinitialise pas les données existantes"""
        tracker = ControlsTracker()
        tracker.initialize()

        # Modifier un contrôle
        tracker.update_control_status('A.5.1', 'implemented')
        tracker.update_control_notes('A.5.1', 'Already implemented')

        # Réinitialiser
        tracker.initialize()

        # Vérifier que les données sont préservées
        assert tracker.get_control_status('A.5.1') == 'implemented'
        assert tracker.get_control_notes('A.5.1') == 'Already implemented'

    def test_file_path_setup(self, mock_config_dir):
        """Test que le chemin du fichier est correct"""
        tracker = ControlsTracker()
        assert tracker.file_path.name == "controls.yml"
        assert "iso27001" in str(tracker.file_path)


class TestControlsTrackerGetMethods:
    """Tests des méthodes de récupération"""

    def test_get_control_status_existing(self, mock_config_dir):
        """Test récupération du statut d'un contrôle existant"""
        tracker = ControlsTracker()
        tracker.initialize()

        status = tracker.get_control_status('A.5.1')
        assert status == 'not_started'

    def test_get_control_status_nonexistent(self, mock_config_dir):
        """Test récupération du statut d'un contrôle inexistant"""
        tracker = ControlsTracker()

        status = tracker.get_control_status('A.99.99')
        assert status == 'not_started'

    def test_get_control_priority_existing(self, mock_config_dir):
        """Test récupération de la priorité"""
        tracker = ControlsTracker()
        tracker.initialize()

        priority = tracker.get_control_priority('A.5.1')
        assert priority == 'medium'

    def test_get_control_priority_nonexistent(self, mock_config_dir):
        """Test récupération priorité d'un contrôle inexistant"""
        tracker = ControlsTracker()

        priority = tracker.get_control_priority('A.99.99')
        assert priority == 'medium'

    def test_get_control_notes_existing(self, mock_config_dir):
        """Test récupération des notes"""
        tracker = ControlsTracker()
        tracker.initialize()

        notes = tracker.get_control_notes('A.5.1')
        assert notes == ''

    def test_get_control_evidence_existing(self, mock_config_dir):
        """Test récupération des preuves"""
        tracker = ControlsTracker()
        tracker.initialize()

        evidence = tracker.get_control_evidence('A.5.1')
        assert evidence == []

    def test_get_control_evidence_nonexistent(self, mock_config_dir):
        """Test récupération preuves d'un contrôle inexistant"""
        tracker = ControlsTracker()

        evidence = tracker.get_control_evidence('A.99.99')
        assert evidence == []


class TestControlsTrackerUpdateStatus:
    """Tests de mise à jour du statut"""

    def test_update_status_from_not_started(self, mock_config_dir):
        """Test mise à jour du statut depuis not_started"""
        tracker = ControlsTracker()
        tracker.initialize()

        tracker.update_control_status('A.5.1', 'in_progress')

        assert tracker.get_control_status('A.5.1') == 'in_progress'

    def test_update_status_to_implemented_sets_date(self, mock_config_dir):
        """Test que passer à implemented définit la date"""
        tracker = ControlsTracker()
        tracker.initialize()

        tracker.update_control_status('A.5.1', 'implemented')

        control_data = tracker.data['controls']['A.5.1']
        assert control_data['implementation_date'] is not None

        # Vérifier format ISO
        datetime.fromisoformat(control_data['implementation_date'])

    def test_update_status_nonexistent_control(self, mock_config_dir):
        """Test mise à jour du statut d'un contrôle inexistant"""
        tracker = ControlsTracker()

        tracker.update_control_status('A.99.99', 'implemented')

        assert tracker.get_control_status('A.99.99') == 'implemented'
        assert 'A.99.99' in tracker.data['controls']

    def test_update_status_all_states(self, mock_config_dir):
        """Test tous les états possibles"""
        tracker = ControlsTracker()
        tracker.initialize()

        states = ['not_started', 'in_progress', 'implemented', 'verified']

        for state in states:
            tracker.update_control_status('A.5.1', state)
            assert tracker.get_control_status('A.5.1') == state


class TestControlsTrackerUpdatePriority:
    """Tests de mise à jour de la priorité"""

    def test_update_priority_existing(self, mock_config_dir):
        """Test mise à jour priorité d'un contrôle existant"""
        tracker = ControlsTracker()
        tracker.initialize()

        tracker.update_control_priority('A.5.1', 'high')

        assert tracker.get_control_priority('A.5.1') == 'high'

    def test_update_priority_nonexistent(self, mock_config_dir):
        """Test mise à jour priorité d'un contrôle inexistant"""
        tracker = ControlsTracker()

        tracker.update_control_priority('A.99.99', 'critical')

        assert tracker.get_control_priority('A.99.99') == 'critical'

    def test_update_priority_all_levels(self, mock_config_dir):
        """Test tous les niveaux de priorité"""
        tracker = ControlsTracker()
        tracker.initialize()

        priorities = ['low', 'medium', 'high', 'critical']

        for priority in priorities:
            tracker.update_control_priority('A.5.1', priority)
            assert tracker.get_control_priority('A.5.1') == priority


class TestControlsTrackerUpdateNotes:
    """Tests de mise à jour des notes"""

    def test_update_notes_existing(self, mock_config_dir):
        """Test mise à jour des notes"""
        tracker = ControlsTracker()
        tracker.initialize()

        tracker.update_control_notes('A.5.1', 'Politique formellement approuvée')

        assert tracker.get_control_notes('A.5.1') == 'Politique formellement approuvée'

    def test_update_notes_nonexistent(self, mock_config_dir):
        """Test mise à jour notes d'un contrôle inexistant"""
        tracker = ControlsTracker()

        tracker.update_control_notes('A.99.99', 'Test notes')

        assert tracker.get_control_notes('A.99.99') == 'Test notes'

    def test_update_notes_multiline(self, mock_config_dir):
        """Test notes multi-lignes"""
        tracker = ControlsTracker()
        tracker.initialize()

        multiline_notes = """
        Ligne 1: Description
        Ligne 2: Détails
        Ligne 3: Plus d'info
        """

        tracker.update_control_notes('A.5.1', multiline_notes)

        assert tracker.get_control_notes('A.5.1') == multiline_notes

    def test_update_notes_empty_string(self, mock_config_dir):
        """Test mise à jour avec chaîne vide"""
        tracker = ControlsTracker()
        tracker.initialize()

        tracker.update_control_notes('A.5.1', 'Some notes')
        tracker.update_control_notes('A.5.1', '')

        assert tracker.get_control_notes('A.5.1') == ''


class TestControlsTrackerAddEvidence:
    """Tests d'ajout de preuves"""

    def test_add_evidence_single(self, mock_config_dir):
        """Test ajout d'une seule preuve"""
        tracker = ControlsTracker()
        tracker.initialize()

        tracker.add_control_evidence('A.5.1', ['Document1.pdf'])

        evidence = tracker.get_control_evidence('A.5.1')
        assert len(evidence) == 1
        assert 'Document1.pdf' in evidence

    def test_add_evidence_multiple(self, mock_config_dir):
        """Test ajout de plusieurs preuves"""
        tracker = ControlsTracker()
        tracker.initialize()

        tracker.add_control_evidence('A.5.1', ['Doc1.pdf', 'Doc2.pdf', 'Doc3.pdf'])

        evidence = tracker.get_control_evidence('A.5.1')
        assert len(evidence) == 3

    def test_add_evidence_accumulates(self, mock_config_dir):
        """Test que les preuves s'accumulent"""
        tracker = ControlsTracker()
        tracker.initialize()

        tracker.add_control_evidence('A.5.1', ['Doc1.pdf'])
        tracker.add_control_evidence('A.5.1', ['Doc2.pdf'])
        tracker.add_control_evidence('A.5.1', ['Doc3.pdf'])

        evidence = tracker.get_control_evidence('A.5.1')
        assert len(evidence) == 3
        assert 'Doc1.pdf' in evidence
        assert 'Doc2.pdf' in evidence
        assert 'Doc3.pdf' in evidence

    def test_add_evidence_nonexistent_control(self, mock_config_dir):
        """Test ajout de preuves pour contrôle inexistant"""
        tracker = ControlsTracker()

        tracker.add_control_evidence('A.99.99', ['Document.pdf'])

        evidence = tracker.get_control_evidence('A.99.99')
        assert len(evidence) == 1
        assert 'Document.pdf' in evidence

    def test_add_evidence_empty_list(self, mock_config_dir):
        """Test ajout d'une liste vide"""
        tracker = ControlsTracker()
        tracker.initialize()

        tracker.add_control_evidence('A.5.1', [])

        evidence = tracker.get_control_evidence('A.5.1')
        assert evidence == []


class TestControlsTrackerStatistics:
    """Tests des statistiques"""

    def test_get_statistics_empty(self, mock_config_dir):
        """Test statistiques sur tracker vide"""
        tracker = ControlsTracker()

        stats = tracker.get_statistics()

        assert stats['total'] == 0
        assert stats['not_started'] == 0
        assert stats['in_progress'] == 0
        assert stats['implemented'] == 0
        assert stats['verified'] == 0

    def test_get_statistics_after_init(self, mock_config_dir):
        """Test statistiques après initialisation"""
        tracker = ControlsTracker()
        tracker.initialize()

        stats = tracker.get_statistics()

        all_controls = get_all_controls()
        assert stats['total'] == len(all_controls)
        assert stats['not_started'] == len(all_controls)
        assert stats['in_progress'] == 0
        assert stats['implemented'] == 0
        assert stats['verified'] == 0

    def test_get_statistics_with_updates(self, mock_config_dir):
        """Test statistiques avec mises à jour"""
        tracker = ControlsTracker()
        tracker.initialize()

        # Mettre à jour quelques contrôles
        tracker.update_control_status('A.5.1', 'implemented')
        tracker.update_control_status('A.5.2', 'implemented')
        tracker.update_control_status('A.5.3', 'implemented')
        tracker.update_control_status('A.6.1', 'in_progress')
        tracker.update_control_status('A.6.2', 'in_progress')
        tracker.update_control_status('A.7.1', 'verified')

        stats = tracker.get_statistics()

        assert stats['implemented'] == 3
        assert stats['in_progress'] == 2
        assert stats['verified'] == 1

    def test_get_statistics_all_implemented(self, mock_config_dir):
        """Test statistiques avec tous implémentés"""
        tracker = ControlsTracker()
        tracker.initialize()

        # Marquer tous comme implémentés
        all_controls = get_all_controls()
        for control in all_controls:
            tracker.update_control_status(control['id'], 'implemented')

        stats = tracker.get_statistics()

        assert stats['not_started'] == 0
        assert stats['implemented'] == len(all_controls)


class TestControlsTrackerPersistence:
    """Tests de persistance"""

    def test_save_and_load(self, mock_config_dir):
        """Test sauvegarde et rechargement"""
        tracker1 = ControlsTracker()
        tracker1.initialize()
        tracker1.update_control_status('A.5.1', 'implemented')
        tracker1.update_control_notes('A.5.1', 'Test notes')
        tracker1.save()

        # Créer une nouvelle instance (recharge depuis le fichier)
        tracker2 = ControlsTracker()

        assert tracker2.get_control_status('A.5.1') == 'implemented'
        assert tracker2.get_control_notes('A.5.1') == 'Test notes'

    def test_last_updated_timestamp(self, mock_config_dir):
        """Test que last_updated est mis à jour"""
        tracker = ControlsTracker()
        tracker.initialize()

        assert tracker.data['last_updated'] is not None
        datetime.fromisoformat(tracker.data['last_updated'])

    def test_save_updates_timestamp(self, mock_config_dir):
        """Test que save() met à jour le timestamp"""
        tracker = ControlsTracker()
        tracker.initialize()

        original_timestamp = tracker.data['last_updated']

        import time
        time.sleep(0.01)

        tracker.save()

        assert tracker.data['last_updated'] != original_timestamp


class TestControlsTrackerIntegration:
    """Tests d'intégration avec controls_data"""

    def test_all_iso_controls_created(self, mock_config_dir):
        """Test que tous les contrôles ISO 27001:2022 sont créés"""
        tracker = ControlsTracker()
        tracker.initialize()

        # Vérifier les 4 catégories
        categories = {
            'A.5': 37,  # Organisationnels
            'A.6': 8,   # Personnes
            'A.7': 14,  # Physiques
            'A.8': 34   # Technologiques
        }

        for category, expected_count in categories.items():
            count = sum(1 for cid in tracker.data['controls'].keys()
                       if cid.startswith(category + '.'))
            assert count == expected_count, f"Expected {expected_count} controls in {category}, got {count}"

    def test_specific_controls_exist(self, mock_config_dir):
        """Test que des contrôles spécifiques existent"""
        tracker = ControlsTracker()
        tracker.initialize()

        specific_controls = [
            'A.5.1',   # Politiques de sécurité
            'A.5.15',  # Contrôle d'accès
            'A.6.1',   # Sélection
            'A.7.1',   # Périmètres de sécurité
            'A.8.1',   # Équipements terminaux
        ]

        for control_id in specific_controls:
            assert control_id in tracker.data['controls']
            assert tracker.get_control_status(control_id) == 'not_started'


class TestControlsTrackerEdgeCases:
    """Tests de cas limites"""

    def test_multiple_evidence_types(self, mock_config_dir):
        """Test différents types de preuves"""
        tracker = ControlsTracker()
        tracker.initialize()

        evidence_list = [
            'policy_v1.0.pdf',
            'training_certificate.jpg',
            'audit_log_2024.xlsx',
            'https://internal.wiki/security-policy',
            'email_approval_20240115.eml'
        ]

        tracker.add_control_evidence('A.5.1', evidence_list)

        evidence = tracker.get_control_evidence('A.5.1')
        assert len(evidence) == 5
        for item in evidence_list:
            assert item in evidence

    def test_long_notes(self, mock_config_dir):
        """Test avec notes très longues"""
        tracker = ControlsTracker()
        tracker.initialize()

        long_notes = "A" * 10000  # 10,000 caractères

        tracker.update_control_notes('A.5.1', long_notes)

        assert len(tracker.get_control_notes('A.5.1')) == 10000

    def test_special_characters_in_notes(self, mock_config_dir):
        """Test caractères spéciaux dans les notes"""
        tracker = ControlsTracker()
        tracker.initialize()

        special_notes = "Notes avec émojis 🔒🛡️ et caractères spéciaux: éàç <>&\""

        tracker.update_control_notes('A.5.1', special_notes)

        assert tracker.get_control_notes('A.5.1') == special_notes

    def test_update_all_fields_together(self, mock_config_dir):
        """Test mise à jour de tous les champs ensemble"""
        tracker = ControlsTracker()
        tracker.initialize()

        tracker.update_control_status('A.5.1', 'verified')
        tracker.update_control_priority('A.5.1', 'critical')
        tracker.update_control_notes('A.5.1', 'Fully implemented and verified')
        tracker.add_control_evidence('A.5.1', ['proof1.pdf', 'proof2.pdf'])

        control_data = tracker.data['controls']['A.5.1']

        assert control_data['status'] == 'verified'
        assert control_data['priority'] == 'critical'
        assert control_data['notes'] == 'Fully implemented and verified'
        assert len(control_data['evidence']) == 2
