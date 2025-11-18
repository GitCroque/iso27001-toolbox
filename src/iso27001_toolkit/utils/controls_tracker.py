"""
Tracker pour le suivi de l'implémentation des contrôles ISO 27001
"""

import yaml
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

from iso27001_toolkit.utils.config import get_controls_file
from iso27001_toolkit.utils.controls_data import get_all_controls


class ControlsTracker:
    """Gestionnaire de suivi des contrôles"""

    def __init__(self):
        self.file_path = get_controls_file()
        self.data = self._load()

    def _load(self) -> Dict:
        """Charge les données de suivi des contrôles"""
        if not self.file_path.exists():
            return {'controls': {}, 'last_updated': None}

        with open(self.file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {'controls': {}, 'last_updated': None}

    def save(self):
        """Sauvegarde les données de suivi"""
        self.data['last_updated'] = datetime.now().isoformat()

        with open(self.file_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.data, f, allow_unicode=True, default_flow_style=False)

    def initialize(self):
        """Initialise le suivi des contrôles avec tous les contrôles ISO 27001"""
        all_controls = get_all_controls()

        for control in all_controls:
            control_id = control['id']
            if control_id not in self.data['controls']:
                self.data['controls'][control_id] = {
                    'status': 'not_started',
                    'priority': 'medium',
                    'notes': '',
                    'evidence': [],
                    'responsible_party': '',
                    'implementation_date': None,
                    'review_date': None
                }

        self.save()

    def get_control_status(self, control_id: str) -> str:
        """Retourne le statut d'un contrôle"""
        return self.data['controls'].get(control_id, {}).get('status', 'not_started')

    def get_control_priority(self, control_id: str) -> str:
        """Retourne la priorité d'un contrôle"""
        return self.data['controls'].get(control_id, {}).get('priority', 'medium')

    def get_control_notes(self, control_id: str) -> str:
        """Retourne les notes d'un contrôle"""
        return self.data['controls'].get(control_id, {}).get('notes', '')

    def get_control_evidence(self, control_id: str) -> List[str]:
        """Retourne les preuves d'un contrôle"""
        return self.data['controls'].get(control_id, {}).get('evidence', [])

    def update_control_status(self, control_id: str, status: str):
        """Met à jour le statut d'un contrôle"""
        if control_id not in self.data['controls']:
            self.data['controls'][control_id] = {}

        self.data['controls'][control_id]['status'] = status

        if status == 'implemented':
            self.data['controls'][control_id]['implementation_date'] = datetime.now().isoformat()

    def update_control_priority(self, control_id: str, priority: str):
        """Met à jour la priorité d'un contrôle"""
        if control_id not in self.data['controls']:
            self.data['controls'][control_id] = {}

        self.data['controls'][control_id]['priority'] = priority

    def update_control_notes(self, control_id: str, notes: str):
        """Met à jour les notes d'un contrôle"""
        if control_id not in self.data['controls']:
            self.data['controls'][control_id] = {}

        self.data['controls'][control_id]['notes'] = notes

    def add_control_evidence(self, control_id: str, evidence: List[str]):
        """Ajoute des preuves pour un contrôle"""
        if control_id not in self.data['controls']:
            self.data['controls'][control_id] = {'evidence': []}

        if 'evidence' not in self.data['controls'][control_id]:
            self.data['controls'][control_id]['evidence'] = []

        self.data['controls'][control_id]['evidence'].extend(evidence)

    def get_statistics(self) -> Dict[str, int]:
        """Retourne les statistiques sur les contrôles"""
        stats = {
            'total': 0,
            'not_started': 0,
            'in_progress': 0,
            'implemented': 0,
            'verified': 0
        }

        for control_id, control_data in self.data['controls'].items():
            stats['total'] += 1
            status = control_data.get('status', 'not_started')
            stats[status] = stats.get(status, 0) + 1

        return stats
