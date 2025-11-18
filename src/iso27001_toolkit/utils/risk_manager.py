"""
Gestionnaire de risques pour ISO 27001
"""

import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

from iso27001_toolkit.utils.config import get_risks_file


class RiskManager:
    """Gestionnaire de risques de sécurité de l'information"""

    def __init__(self):
        self.file_path = get_risks_file()
        self.data = self._load()

    def _load(self) -> Dict:
        """Charge les données de risques"""
        if not self.file_path.exists():
            return {'risks': [], 'last_updated': None}

        with open(self.file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {'risks': [], 'last_updated': None}

    def save(self):
        """Sauvegarde les données de risques"""
        self.data['last_updated'] = datetime.now().isoformat()

        with open(self.file_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    def initialize(self):
        """Initialise le registre des risques"""
        if not self.data.get('risks'):
            self.data['risks'] = []

        # Ajouter quelques risques exemples si le registre est vide
        if len(self.data['risks']) == 0:
            example_risks = [
                {
                    'id': 'RISK-001',
                    'name': 'Accès non autorisé aux données sensibles',
                    'description': 'Un utilisateur non autorisé pourrait accéder à des données sensibles de l\'organisation',
                    'category': 'confidentiality',
                    'assets': ['Base de données client', 'Fichiers RH'],
                    'impact': 4,
                    'likelihood': 3,
                    'risk_score': 12,
                    'risk_level': 'high',
                    'status': 'identified',
                    'treatment': 'mitigate',
                    'mitigation_measures': [
                        'Implémentation de contrôles d\'accès basés sur les rôles',
                        'Authentification multi-facteurs',
                        'Chiffrement des données sensibles'
                    ],
                    'controls': ['A.5.15', 'A.5.16', 'A.8.5'],
                    'owner': '',
                    'review_date': (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d'),
                    'created_at': datetime.now().isoformat()
                }
            ]
            self.data['risks'] = example_risks

        self.save()

    def _generate_risk_id(self) -> str:
        """Génère un ID unique pour un risque"""
        existing_ids = [r['id'] for r in self.data['risks']]
        counter = 1

        while True:
            risk_id = f"RISK-{counter:03d}"
            if risk_id not in existing_ids:
                return risk_id
            counter += 1

    def _calculate_risk_score(self, impact: int, likelihood: int) -> tuple:
        """Calcule le score et le niveau de risque"""
        score = impact * likelihood

        if score >= 16:
            level = 'critical'
        elif score >= 10:
            level = 'high'
        elif score >= 5:
            level = 'medium'
        else:
            level = 'low'

        return score, level

    def add_risk(self, risk_data: Dict) -> str:
        """Ajoute un nouveau risque"""
        risk_id = self._generate_risk_id()

        impact = risk_data.get('impact', 3)
        likelihood = risk_data.get('likelihood', 3)
        score, level = self._calculate_risk_score(impact, likelihood)

        new_risk = {
            'id': risk_id,
            'name': risk_data.get('name', 'Nouveau risque'),
            'description': risk_data.get('description', ''),
            'category': risk_data.get('category', 'operational'),
            'assets': risk_data.get('assets', []),
            'impact': impact,
            'likelihood': likelihood,
            'risk_score': score,
            'risk_level': level,
            'status': risk_data.get('status', 'identified'),
            'treatment': risk_data.get('treatment', 'mitigate'),
            'mitigation_measures': risk_data.get('mitigation_measures', []),
            'controls': risk_data.get('controls', []),
            'owner': risk_data.get('owner', ''),
            'review_date': risk_data.get('review_date', (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }

        self.data['risks'].append(new_risk)
        self.save()

        return risk_id

    def get_risk(self, risk_id: str) -> Optional[Dict]:
        """Retourne un risque spécifique"""
        for risk in self.data['risks']:
            if risk['id'] == risk_id:
                return risk
        return None

    def get_all_risks(self) -> List[Dict]:
        """Retourne tous les risques"""
        return self.data['risks']

    def update_risk(self, risk_id: str, updates: Dict):
        """Met à jour un risque"""
        for risk in self.data['risks']:
            if risk['id'] == risk_id:
                # Mettre à jour les champs
                for key, value in updates.items():
                    risk[key] = value

                # Recalculer le score si nécessaire
                if 'impact' in updates or 'likelihood' in updates:
                    impact = risk.get('impact', 3)
                    likelihood = risk.get('likelihood', 3)
                    score, level = self._calculate_risk_score(impact, likelihood)
                    risk['risk_score'] = score
                    risk['risk_level'] = level

                risk['updated_at'] = datetime.now().isoformat()
                self.save()
                return True

        return False

    def delete_risk(self, risk_id: str) -> bool:
        """Supprime un risque"""
        initial_len = len(self.data['risks'])
        self.data['risks'] = [r for r in self.data['risks'] if r['id'] != risk_id]

        if len(self.data['risks']) < initial_len:
            self.save()
            return True

        return False

    def get_risks_by_level(self, level: str) -> List[Dict]:
        """Retourne les risques d'un niveau donné"""
        return [r for r in self.data['risks'] if r.get('risk_level') == level]

    def get_risks_by_category(self, category: str) -> List[Dict]:
        """Retourne les risques d'une catégorie donnée"""
        return [r for r in self.data['risks'] if r.get('category') == category]

    def get_statistics(self) -> Dict:
        """Retourne les statistiques sur les risques"""
        stats = {
            'total': len(self.data['risks']),
            'by_level': {'critical': 0, 'high': 0, 'medium': 0, 'low': 0},
            'by_status': {},
            'by_treatment': {}
        }

        for risk in self.data['risks']:
            # Par niveau
            level = risk.get('risk_level', 'medium')
            stats['by_level'][level] = stats['by_level'].get(level, 0) + 1

            # Par statut
            status = risk.get('status', 'identified')
            stats['by_status'][status] = stats['by_status'].get(status, 0) + 1

            # Par traitement
            treatment = risk.get('treatment', 'mitigate')
            stats['by_treatment'][treatment] = stats['by_treatment'].get(treatment, 0) + 1

        return stats
