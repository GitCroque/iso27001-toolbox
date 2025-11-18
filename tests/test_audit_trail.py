"""
Tests pour le module d'audit trail

Tests critiques pour certification ISO 27001:
- Who/When/What/Where/Result
- Immuabilité (append-only)
- Filtrage et query
- Export pour audits
"""

import os
import pytest
from datetime import datetime, timedelta
from pathlib import Path

from iso27001_toolkit.utils.audit_trail import (
    AuditTrail,
    AuditAction,
    AuditLevel,
    get_audit_trail,
    _reset_audit_trail_singleton
)


@pytest.fixture(autouse=True)
def reset_singleton():
    """Réinitialise le singleton avant chaque test"""
    _reset_audit_trail_singleton()
    yield
    _reset_audit_trail_singleton()


class TestAuditTrailBasics:
    """Tests de base de l'audit trail"""

    def test_audit_trail_initialization(self, mock_config_dir):
        """Test que l'audit trail s'initialise correctement"""
        audit = AuditTrail()

        assert audit.audit_file.exists()
        assert audit.current_user is not None

    def test_audit_file_has_restrictive_permissions(self, mock_config_dir):
        """Test que le fichier d'audit a des permissions restrictives"""
        audit = AuditTrail()

        # Vérifier permissions (0600)
        import stat
        permissions = stat.S_IMODE(os.stat(audit.audit_file).st_mode)
        assert permissions == 0o600, f"Expected 0600, got {oct(permissions)}"

    def test_log_simple_entry(self, mock_config_dir):
        """Test d'enregistrement d'une entrée simple"""
        audit = AuditTrail()

        audit.log(
            action=AuditAction.RISK_CREATED,
            entity_type='risk',
            entity_id='RISK-001',
            details={'name': 'Test Risk'}
        )

        # Vérifier que l'entrée existe
        entries = audit.get_entries()
        assert len(entries) == 1
        assert entries[0]['action'] == AuditAction.RISK_CREATED.value
        assert entries[0]['entity_id'] == 'RISK-001'
        assert entries[0]['success'] is True

    def test_log_entry_contains_who_when_what(self, mock_config_dir):
        """Test que chaque entrée contient Who/When/What/Where"""
        audit = AuditTrail()

        audit.log(
            action=AuditAction.CONTROL_STATUS_UPDATED,
            entity_type='control',
            entity_id='A.5.1',
            details={'old_status': 'not_started', 'new_status': 'in_progress'}
        )

        entries = audit.get_entries()
        entry = entries[0]

        # Who
        assert 'user' in entry
        assert entry['user'] == audit.current_user

        # When
        assert 'timestamp' in entry
        timestamp = datetime.fromisoformat(entry['timestamp'])
        assert (datetime.now() - timestamp).total_seconds() < 5

        # What
        assert 'action' in entry
        assert entry['action'] == AuditAction.CONTROL_STATUS_UPDATED.value

        # Where
        assert 'entity_type' in entry
        assert 'entity_id' in entry
        assert entry['entity_type'] == 'control'
        assert entry['entity_id'] == 'A.5.1'

        # Result
        assert 'success' in entry
        assert entry['success'] is True

    def test_log_failure(self, mock_config_dir):
        """Test d'enregistrement d'un échec"""
        audit = AuditTrail()

        audit.log(
            action=AuditAction.RISK_DELETED,
            entity_type='risk',
            entity_id='RISK-999',
            success=False,
            error_message="Risk not found",
            level=AuditLevel.WARNING
        )

        entries = audit.get_entries()
        entry = entries[0]

        assert entry['success'] is False
        assert entry['error_message'] == "Risk not found"
        assert entry['level'] == AuditLevel.WARNING.value


class TestAuditTrailFiltering:
    """Tests de filtrage de l'audit trail"""

    def test_filter_by_user(self, mock_config_dir):
        """Test filtrage par utilisateur"""
        audit = AuditTrail()

        # Créer des entrées
        audit.log(AuditAction.RISK_CREATED, 'risk', 'RISK-001')
        audit.log(AuditAction.RISK_UPDATED, 'risk', 'RISK-002')

        # Filtrer par utilisateur
        entries = audit.get_entries(user=audit.current_user)
        assert len(entries) == 2

        entries_other = audit.get_entries(user='nonexistent_user')
        assert len(entries_other) == 0

    def test_filter_by_action(self, mock_config_dir):
        """Test filtrage par action"""
        audit = AuditTrail()

        audit.log(AuditAction.RISK_CREATED, 'risk', 'RISK-001')
        audit.log(AuditAction.RISK_UPDATED, 'risk', 'RISK-001')
        audit.log(AuditAction.RISK_DELETED, 'risk', 'RISK-001')

        # Filtrer par action
        created = audit.get_entries(action=AuditAction.RISK_CREATED)
        assert len(created) == 1

        updated = audit.get_entries(action=AuditAction.RISK_UPDATED)
        assert len(updated) == 1

    def test_filter_by_entity(self, mock_config_dir):
        """Test filtrage par entité"""
        audit = AuditTrail()

        audit.log(AuditAction.RISK_CREATED, 'risk', 'RISK-001')
        audit.log(AuditAction.RISK_CREATED, 'risk', 'RISK-002')
        audit.log(AuditAction.CONTROL_STATUS_UPDATED, 'control', 'A.5.1')

        # Filtrer par type d'entité
        risks = audit.get_entries(entity_type='risk')
        assert len(risks) == 2

        controls = audit.get_entries(entity_type='control')
        assert len(controls) == 1

        # Filtrer par ID spécifique
        risk_001 = audit.get_entries(entity_id='RISK-001')
        assert len(risk_001) == 1
        assert risk_001[0]['entity_id'] == 'RISK-001'

    def test_filter_by_level(self, mock_config_dir):
        """Test filtrage par niveau"""
        audit = AuditTrail()

        audit.log(AuditAction.RISK_CREATED, 'risk', 'RISK-001', level=AuditLevel.INFO)
        audit.log(AuditAction.RISK_DELETED, 'risk', 'RISK-002', level=AuditLevel.WARNING)
        audit.log(
            AuditAction.ENCRYPTION_KEY_ROTATED,
            'system',
            None,
            level=AuditLevel.CRITICAL
        )

        # Filtrer par niveau
        info_entries = audit.get_entries(level=AuditLevel.INFO)
        assert len(info_entries) == 1

        critical_entries = audit.get_entries(level=AuditLevel.CRITICAL)
        assert len(critical_entries) == 1

    def test_filter_by_date_range(self, mock_config_dir):
        """Test filtrage par plage de dates"""
        audit = AuditTrail()

        now = datetime.now()
        yesterday = now - timedelta(days=1)
        tomorrow = now + timedelta(days=1)

        audit.log(AuditAction.RISK_CREATED, 'risk', 'RISK-001')

        # Filtrer depuis hier (devrait trouver)
        entries_since = audit.get_entries(since=yesterday)
        assert len(entries_since) == 1

        # Filtrer depuis demain (ne devrait rien trouver)
        entries_future = audit.get_entries(since=tomorrow)
        assert len(entries_future) == 0

        # Filtrer jusqu'à demain (devrait trouver)
        entries_until = audit.get_entries(until=tomorrow)
        assert len(entries_until) == 1

    def test_filter_with_limit(self, mock_config_dir):
        """Test limitation du nombre de résultats"""
        audit = AuditTrail()

        # Créer 10 entrées
        for i in range(10):
            audit.log(AuditAction.RISK_CREATED, 'risk', f'RISK-{i:03d}')

        # Limiter à 5
        entries = audit.get_entries(limit=5)
        assert len(entries) == 5

        # Vérifier que c'est les plus récentes (ordre inverse)
        assert entries[0]['entity_id'] == 'RISK-009'
        assert entries[4]['entity_id'] == 'RISK-005'


class TestAuditTrailEntityHistory:
    """Tests de l'historique d'une entité"""

    def test_get_entity_complete_history(self, mock_config_dir):
        """Test récupération de l'historique complet d'une entité"""
        audit = AuditTrail()

        # Cycle de vie d'un risque
        audit.log(AuditAction.RISK_CREATED, 'risk', 'RISK-001', details={'name': 'Initial'})
        audit.log(
            AuditAction.RISK_UPDATED,
            'risk',
            'RISK-001',
            details={'field': 'impact', 'old': 3, 'new': 5}
        )
        audit.log(
            AuditAction.RISK_STATUS_CHANGED,
            'risk',
            'RISK-001',
            details={'old_status': 'open', 'new_status': 'mitigated'}
        )

        # Récupérer l'historique
        history = audit.get_entity_history('risk', 'RISK-001')

        assert len(history) == 3
        # Ordre chronologique inverse (plus récent en premier)
        assert history[0]['action'] == AuditAction.RISK_STATUS_CHANGED.value
        assert history[1]['action'] == AuditAction.RISK_UPDATED.value
        assert history[2]['action'] == AuditAction.RISK_CREATED.value

    def test_entity_history_shows_modifications(self, mock_config_dir):
        """Test que l'historique montre toutes les modifications"""
        audit = AuditTrail()

        # Multiples updates
        for i in range(5):
            audit.log(
                AuditAction.CONTROL_STATUS_UPDATED,
                'control',
                'A.5.1',
                details={'iteration': i}
            )

        history = audit.get_entity_history('control', 'A.5.1')
        assert len(history) == 5


class TestAuditTrailUserActivity:
    """Tests de l'activité utilisateur"""

    def test_get_user_activity(self, mock_config_dir):
        """Test récupération de l'activité d'un utilisateur"""
        audit = AuditTrail()
        user = audit.current_user

        audit.log(AuditAction.RISK_CREATED, 'risk', 'RISK-001')
        audit.log(AuditAction.CONTROL_STATUS_UPDATED, 'control', 'A.5.1')
        audit.log(AuditAction.POLICY_GENERATED, 'policy', 'access_control')

        activity = audit.get_user_activity(user)
        assert len(activity) == 3

    def test_user_activity_with_date_range(self, mock_config_dir):
        """Test activité utilisateur avec plage de dates"""
        audit = AuditTrail()
        user = audit.current_user

        audit.log(AuditAction.RISK_CREATED, 'risk', 'RISK-001')

        yesterday = datetime.now() - timedelta(days=1)
        activity_recent = audit.get_user_activity(user, since=yesterday)
        assert len(activity_recent) == 1

        tomorrow = datetime.now() + timedelta(days=1)
        activity_future = audit.get_user_activity(user, since=tomorrow)
        assert len(activity_future) == 0


class TestAuditTrailCriticalEvents:
    """Tests des événements critiques"""

    def test_get_critical_events(self, mock_config_dir):
        """Test récupération des événements critiques"""
        audit = AuditTrail()

        # Événements normaux
        audit.log(AuditAction.RISK_CREATED, 'risk', 'RISK-001', level=AuditLevel.INFO)
        audit.log(AuditAction.RISK_UPDATED, 'risk', 'RISK-001', level=AuditLevel.INFO)

        # Événements critiques
        audit.log(
            AuditAction.ENCRYPTION_KEY_ROTATED,
            'system',
            None,
            level=AuditLevel.CRITICAL
        )
        audit.log(
            AuditAction.RISK_DELETED,
            'risk',
            'RISK-999',
            level=AuditLevel.CRITICAL,
            success=False,
            error_message="Unauthorized deletion attempt"
        )

        critical = audit.get_critical_events()
        assert len(critical) == 2
        assert all(e['level'] == AuditLevel.CRITICAL.value for e in critical)


class TestAuditTrailExport:
    """Tests d'export de l'audit trail"""

    def test_export_for_audit(self, mock_config_dir, tmp_path):
        """Test export de l'audit trail pour audit externe"""
        audit = AuditTrail()

        # Créer des entrées
        audit.log(AuditAction.RISK_CREATED, 'risk', 'RISK-001')
        audit.log(AuditAction.CONTROL_STATUS_UPDATED, 'control', 'A.5.1')
        audit.log(AuditAction.POLICY_GENERATED, 'policy', 'access_control')

        # Exporter
        output_file = tmp_path / "audit_export.yml"
        result = audit.export_for_audit(output_file)

        assert result.exists()
        assert result == output_file

        # Vérifier le contenu
        import yaml
        with open(output_file) as f:
            data = yaml.safe_load(f)

        assert 'export_date' in data
        assert 'export_user' in data
        assert 'total_entries' in data
        assert 'entries' in data
        assert data['total_entries'] == 3

    def test_export_with_date_range(self, mock_config_dir, tmp_path):
        """Test export avec plage de dates"""
        audit = AuditTrail()

        audit.log(AuditAction.RISK_CREATED, 'risk', 'RISK-001')
        audit.log(AuditAction.RISK_CREATED, 'risk', 'RISK-002')

        yesterday = datetime.now() - timedelta(days=1)
        tomorrow = datetime.now() + timedelta(days=1)

        output_file = tmp_path / "audit_range.yml"
        audit.export_for_audit(output_file, since=yesterday, until=tomorrow)

        import yaml
        with open(output_file) as f:
            data = yaml.safe_load(f)

        assert data['total_entries'] == 2


class TestAuditTrailStatistics:
    """Tests des statistiques d'audit"""

    def test_get_statistics(self, mock_config_dir):
        """Test génération de statistiques"""
        audit = AuditTrail()

        # Créer des entrées variées
        audit.log(AuditAction.RISK_CREATED, 'risk', 'RISK-001', success=True)
        audit.log(AuditAction.RISK_UPDATED, 'risk', 'RISK-001', success=True)
        audit.log(AuditAction.RISK_DELETED, 'risk', 'RISK-001', success=False)
        audit.log(AuditAction.CONTROL_STATUS_UPDATED, 'control', 'A.5.1', success=True)

        stats = audit.get_statistics()

        assert stats['total_entries'] == 4
        assert stats['successes'] == 3
        assert stats['failures'] == 1
        assert stats['failure_rate'] == 25.0
        assert stats['unique_users'] >= 1
        assert stats['unique_actions'] == 4

    def test_statistics_by_action(self, mock_config_dir):
        """Test statistiques par action"""
        audit = AuditTrail()

        audit.log(AuditAction.RISK_CREATED, 'risk', 'RISK-001')
        audit.log(AuditAction.RISK_CREATED, 'risk', 'RISK-002')
        audit.log(AuditAction.RISK_UPDATED, 'risk', 'RISK-001')

        stats = audit.get_statistics()

        actions = stats['actions']
        assert actions[AuditAction.RISK_CREATED.value] == 2
        assert actions[AuditAction.RISK_UPDATED.value] == 1


class TestAuditTrailImmutability:
    """Tests d'immuabilité de l'audit trail"""

    def test_audit_file_is_append_only(self, mock_config_dir):
        """Test que le fichier d'audit est append-only"""
        audit = AuditTrail()

        audit.log(AuditAction.RISK_CREATED, 'risk', 'RISK-001')
        audit.log(AuditAction.RISK_UPDATED, 'risk', 'RISK-001')

        entries_before = audit.get_entries()
        assert len(entries_before) == 2

        # Ajouter une nouvelle entrée
        audit.log(AuditAction.RISK_DELETED, 'risk', 'RISK-001')

        entries_after = audit.get_entries()
        assert len(entries_after) == 3

        # Vérifier que les anciennes entrées sont toujours là (immuabilité)
        assert entries_after[2]['action'] == entries_before[1]['action']
        assert entries_after[1]['action'] == entries_before[0]['action']


class TestAuditTrailSingleton:
    """Tests du pattern singleton"""

    def test_get_audit_trail_returns_singleton(self, mock_config_dir):
        """Test que get_audit_trail retourne toujours la même instance"""
        audit1 = get_audit_trail()
        audit2 = get_audit_trail()

        assert audit1 is audit2

    def test_singleton_persists_data(self, mock_config_dir):
        """Test que le singleton persiste les données"""
        audit1 = get_audit_trail()
        audit1.log(AuditAction.RISK_CREATED, 'risk', 'RISK-001')

        audit2 = get_audit_trail()
        entries = audit2.get_entries()

        assert len(entries) >= 1


class TestAuditTrailErrorHandling:
    """Tests de gestion d'erreurs"""

    def test_log_does_not_crash_on_error(self, mock_config_dir):
        """Test que log() ne fait pas crasher en cas d'erreur"""
        audit = AuditTrail()

        # Même si l'audit trail échoue, ça ne doit pas lever d'exception
        # (pour ne pas bloquer les opérations principales)
        try:
            audit.log(
                action=AuditAction.RISK_CREATED,
                entity_type='risk',
                entity_id='RISK-001',
                details={'massive_data': 'x' * 1000000}  # Données énormes
            )
        except Exception:
            pytest.fail("log() should not raise exceptions")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
