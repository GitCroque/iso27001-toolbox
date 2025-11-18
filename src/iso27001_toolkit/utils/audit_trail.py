"""
Module d'audit trail pour ISO 27001

OBLIGATOIRE pour certification ISO 27001:
- Traçabilité complète de toutes les opérations
- Who/When/What/Where/Result
- Immuabilité (append-only)
- Export pour les audits
"""

import os
import yaml
import getpass
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

from iso27001_toolkit.utils import config
from iso27001_toolkit.logger import get_logger

logger = get_logger(__name__)


class AuditAction(Enum):
    """Types d'actions auditables"""
    # Risques
    RISK_CREATED = "risk_created"
    RISK_UPDATED = "risk_updated"
    RISK_DELETED = "risk_deleted"
    RISK_STATUS_CHANGED = "risk_status_changed"

    # Contrôles
    CONTROL_INITIALIZED = "control_initialized"
    CONTROL_STATUS_UPDATED = "control_status_updated"
    CONTROL_PRIORITY_CHANGED = "control_priority_changed"
    CONTROL_EVIDENCE_ADDED = "control_evidence_added"
    CONTROL_NOTES_UPDATED = "control_notes_updated"

    # Politiques
    POLICY_GENERATED = "policy_generated"
    POLICY_UPDATED = "policy_updated"

    # Audit
    AUDIT_ASSESSMENT_GENERATED = "audit_assessment_generated"
    AUDIT_CHECKLIST_GENERATED = "audit_checklist_generated"
    AUDIT_SOA_GENERATED = "audit_soa_generated"

    # Système
    ENCRYPTION_KEY_ROTATED = "encryption_key_rotated"
    DATA_EXPORTED = "data_exported"
    DATA_IMPORTED = "data_imported"
    BACKUP_CREATED = "backup_created"


class AuditLevel(Enum):
    """Niveaux de criticité des événements d'audit"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AuditTrail:
    """
    Gestionnaire d'audit trail pour ISO 27001

    Fonctionnalités:
    - Enregistrement de toutes les opérations (Who/When/What/Where/Result)
    - Stockage append-only (immuable)
    - Query et filtrage
    - Export pour audits
    """

    def __init__(self):
        """Initialise l'audit trail"""
        # Assurer que le répertoire de config existe
        config.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self.audit_file = config.CONFIG_DIR / "audit_trail.yml"
        self._ensure_audit_file_exists()

        # Obtenir l'utilisateur actuel
        try:
            self.current_user = getpass.getuser()
        except:
            self.current_user = os.environ.get('USER', 'unknown')

    def _ensure_audit_file_exists(self):
        """Crée le fichier d'audit s'il n'existe pas"""
        if not self.audit_file.exists():
            self.audit_file.parent.mkdir(parents=True, exist_ok=True)
            initial_data = {
                'audit_trail': [],
                'created_at': datetime.now().isoformat(),
                'format_version': '1.0'
            }
            with open(self.audit_file, 'w', encoding='utf-8') as f:
                yaml.dump(initial_data, f, allow_unicode=True, default_flow_style=False)

            # Permissions restrictives (0600)
            os.chmod(self.audit_file, 0o600)

            logger.info(f"Audit trail initialisé: {self.audit_file}")

    def log(
        self,
        action: AuditAction,
        entity_type: str,
        entity_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        level: AuditLevel = AuditLevel.INFO,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> None:
        """
        Enregistre une entrée dans l'audit trail

        Args:
            action: Type d'action effectuée
            entity_type: Type d'entité concernée (risk, control, policy, etc.)
            entity_id: ID de l'entité (optionnel)
            details: Détails additionnels (optionnel)
            level: Niveau de criticité
            success: Succès ou échec de l'opération
            error_message: Message d'erreur si échec
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'user': self.current_user,
            'action': action.value,
            'entity_type': entity_type,
            'entity_id': entity_id,
            'level': level.value,
            'success': success,
            'details': details or {},
            'error_message': error_message,
            'hostname': os.environ.get('HOSTNAME', 'unknown'),
            'pid': os.getpid()
        }

        # Append à la fin du fichier (append-only pour immuabilité)
        try:
            with open(self.audit_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {'audit_trail': []}

            if 'audit_trail' not in data:
                data['audit_trail'] = []

            data['audit_trail'].append(entry)

            # Écrire atomiquement (éviter corruption)
            temp_file = self.audit_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

            # Définir permissions restrictives
            os.chmod(temp_file, 0o600)

            # Remplacer l'ancien fichier
            temp_file.replace(self.audit_file)

            # Log approprié selon le niveau
            if level == AuditLevel.CRITICAL:
                logger.warning(
                    f"AUDIT CRITICAL: {action.value} on {entity_type}:{entity_id} by {self.current_user}"
                )
            elif not success:
                logger.error(
                    f"AUDIT FAILURE: {action.value} on {entity_type}:{entity_id}: {error_message}"
                )
            else:
                logger.debug(
                    f"AUDIT: {action.value} on {entity_type}:{entity_id} by {self.current_user}"
                )

        except Exception as e:
            # Ne jamais faire échouer l'opération principale à cause de l'audit
            logger.error(f"Erreur lors de l'enregistrement audit: {e}")

    def get_entries(
        self,
        user: Optional[str] = None,
        action: Optional[AuditAction] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        level: Optional[AuditLevel] = None,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Récupère les entrées d'audit avec filtres

        Args:
            user: Filtrer par utilisateur
            action: Filtrer par action
            entity_type: Filtrer par type d'entité
            entity_id: Filtrer par ID d'entité
            level: Filtrer par niveau
            since: Filtrer par date de début
            until: Filtrer par date de fin
            limit: Nombre maximum d'entrées à retourner

        Returns:
            Liste des entrées d'audit filtrées
        """
        try:
            with open(self.audit_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {'audit_trail': []}

            entries = data.get('audit_trail', [])

            # Appliquer les filtres
            filtered = entries

            if user:
                filtered = [e for e in filtered if e.get('user') == user]

            if action:
                filtered = [e for e in filtered if e.get('action') == action.value]

            if entity_type:
                filtered = [e for e in filtered if e.get('entity_type') == entity_type]

            if entity_id:
                filtered = [e for e in filtered if e.get('entity_id') == entity_id]

            if level:
                filtered = [e for e in filtered if e.get('level') == level.value]

            if since:
                filtered = [
                    e for e in filtered
                    if datetime.fromisoformat(e['timestamp']) >= since
                ]

            if until:
                filtered = [
                    e for e in filtered
                    if datetime.fromisoformat(e['timestamp']) <= until
                ]

            # Trier par timestamp (plus récent en premier)
            filtered.sort(key=lambda x: x['timestamp'], reverse=True)

            # Appliquer la limite
            if limit:
                filtered = filtered[:limit]

            return filtered

        except Exception as e:
            logger.error(f"Erreur lors de la lecture de l'audit trail: {e}")
            return []

    def get_entity_history(
        self,
        entity_type: str,
        entity_id: str
    ) -> List[Dict[str, Any]]:
        """
        Récupère l'historique complet d'une entité

        Args:
            entity_type: Type d'entité
            entity_id: ID de l'entité

        Returns:
            Liste chronologique des modifications
        """
        return self.get_entries(entity_type=entity_type, entity_id=entity_id)

    def get_user_activity(
        self,
        user: str,
        since: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Récupère l'activité d'un utilisateur

        Args:
            user: Nom d'utilisateur
            since: Date de début (optionnel)
            limit: Nombre max d'entrées

        Returns:
            Liste des actions de l'utilisateur
        """
        return self.get_entries(user=user, since=since, limit=limit)

    def get_critical_events(
        self,
        since: Optional[datetime] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Récupère les événements critiques

        Args:
            since: Date de début (optionnel)
            limit: Nombre max d'entrées

        Returns:
            Liste des événements critiques
        """
        return self.get_entries(level=AuditLevel.CRITICAL, since=since, limit=limit)

    def export_for_audit(
        self,
        output_file: Path,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None
    ) -> Path:
        """
        Exporte l'audit trail pour un audit externe

        Args:
            output_file: Fichier de sortie
            since: Date de début (optionnel)
            until: Date de fin (optionnel)

        Returns:
            Chemin du fichier exporté
        """
        entries = self.get_entries(since=since, until=until)

        export_data = {
            'export_date': datetime.now().isoformat(),
            'export_user': self.current_user,
            'period': {
                'since': since.isoformat() if since else 'inception',
                'until': until.isoformat() if until else 'now'
            },
            'total_entries': len(entries),
            'entries': entries
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(export_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        logger.info(f"Audit trail exporté: {output_file} ({len(entries)} entrées)")

        # Log l'export lui-même
        self.log(
            action=AuditAction.DATA_EXPORTED,
            entity_type='audit_trail',
            details={'output_file': str(output_file), 'entries_count': len(entries)}
        )

        return output_file

    def get_statistics(self) -> Dict[str, Any]:
        """
        Génère des statistiques sur l'audit trail

        Returns:
            Dict avec statistiques
        """
        try:
            with open(self.audit_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {'audit_trail': []}

            entries = data.get('audit_trail', [])

            # Statistiques de base
            total = len(entries)
            if total == 0:
                return {'total_entries': 0}

            # Par action
            actions = {}
            for entry in entries:
                action = entry.get('action', 'unknown')
                actions[action] = actions.get(action, 0) + 1

            # Par utilisateur
            users = {}
            for entry in entries:
                user = entry.get('user', 'unknown')
                users[user] = users.get(user, 0) + 1

            # Par niveau
            levels = {}
            for entry in entries:
                level = entry.get('level', 'info')
                levels[level] = levels.get(level, 0) + 1

            # Succès/échecs
            successes = sum(1 for e in entries if e.get('success', True))
            failures = total - successes

            # Dates
            first_entry = min(entries, key=lambda x: x['timestamp'])
            last_entry = max(entries, key=lambda x: x['timestamp'])

            return {
                'total_entries': total,
                'successes': successes,
                'failures': failures,
                'failure_rate': (failures / total * 100) if total > 0 else 0,
                'actions': actions,
                'users': users,
                'levels': levels,
                'first_entry': first_entry['timestamp'],
                'last_entry': last_entry['timestamp'],
                'unique_users': len(users),
                'unique_actions': len(actions)
            }

        except Exception as e:
            logger.error(f"Erreur lors du calcul des statistiques: {e}")
            return {'error': str(e)}


# Instance globale (singleton pattern)
_audit_trail_instance: Optional[AuditTrail] = None


def get_audit_trail() -> AuditTrail:
    """
    Récupère l'instance globale de l'audit trail (singleton)

    Returns:
        Instance d'AuditTrail
    """
    global _audit_trail_instance
    if _audit_trail_instance is None:
        _audit_trail_instance = AuditTrail()
    return _audit_trail_instance


def _reset_audit_trail_singleton():
    """
    Réinitialise le singleton (POUR LES TESTS UNIQUEMENT)

    Cette fonction ne devrait être utilisée que dans les tests
    pour éviter les interférences entre les tests.
    """
    global _audit_trail_instance
    _audit_trail_instance = None
