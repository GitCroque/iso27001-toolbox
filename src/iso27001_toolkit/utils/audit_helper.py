"""
Assistant pour la préparation d'audits ISO 27001
"""

import yaml
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
from shutil import copy2

from iso27001_toolkit.utils.config import get_audit_file, get_data_dir
from iso27001_toolkit.utils.controls_tracker import ControlsTracker
from iso27001_toolkit.utils.controls_data import get_all_controls
from iso27001_toolkit.utils.risk_manager import RiskManager


class AuditHelper:
    """Assistant pour la préparation et le suivi des audits"""

    def __init__(self):
        self.file_path = get_audit_file()
        self.data = self._load()
        self.controls_tracker = ControlsTracker()
        self.risk_manager = RiskManager()

    def _load(self) -> Dict:
        """Charge les données d'audit"""
        if not self.file_path.exists():
            return {'audits': [], 'checklists': []}

        with open(self.file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {'audits': [], 'checklists': []}

    def save(self):
        """Sauvegarde les données d'audit"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.data, f, allow_unicode=True, default_flow_style=False)

    def generate_checklist(self) -> Dict:
        """Génère une checklist d'audit complète"""
        all_controls = get_all_controls()

        checklist = {
            'generated_at': datetime.now().isoformat(),
            'categories': {}
        }

        # Grouper par catégorie
        for control in all_controls:
            category = control['category']
            if category not in checklist['categories']:
                checklist['categories'][category] = {
                    'name': control['category_name'],
                    'controls': []
                }

            status = self.controls_tracker.get_control_status(control['id'])
            evidence = self.controls_tracker.get_control_evidence(control['id'])

            checklist['categories'][category]['controls'].append({
                'id': control['id'],
                'name': control['name'],
                'status': status,
                'evidence_count': len(evidence),
                'check_items': [
                    'Politique documentée',
                    'Procédure mise en œuvre',
                    'Preuves d\'application',
                    'Revue périodique effectuée'
                ]
            })

        return checklist

    def assess_readiness(self) -> Dict:
        """Évalue le niveau de préparation pour l'audit"""
        stats = self.controls_tracker.get_statistics()

        # Documents requis
        required_docs = [
            {'name': 'Politique de sécurité de l\'information', 'exists': False},
            {'name': 'Politique de contrôle d\'accès', 'exists': False},
            {'name': 'Registre des risques', 'exists': self.risk_manager.get_all_risks() is not None},
            {'name': 'Déclaration d\'applicabilité (SOA)', 'exists': False},
            {'name': 'Plan de traitement des risques', 'exists': False},
            {'name': 'Procédure de gestion des incidents', 'exists': False},
            {'name': 'Plan de continuité d\'activité', 'exists': False},
        ]

        # Calculer le score de préparation
        controls_score = ((stats.get('implemented', 0) + stats.get('verified', 0)) / stats['total'] * 100) if stats['total'] > 0 else 0
        docs_score = (sum(1 for d in required_docs if d['exists']) / len(required_docs) * 100)
        overall_score = (controls_score * 0.7 + docs_score * 0.3)

        # Recommandations
        recommendations = []
        if stats.get('not_started', 0) > 0:
            recommendations.append(f"Démarrer l'implémentation de {stats['not_started']} contrôles non commencés")

        if stats.get('in_progress', 0) > 0:
            recommendations.append(f"Finaliser l'implémentation de {stats['in_progress']} contrôles en cours")

        if docs_score < 100:
            recommendations.append(f"Compléter les documents manquants ({len([d for d in required_docs if not d['exists']])} manquants)")

        return {
            'overall_score': round(overall_score, 1),
            'controls_status': stats,
            'required_documents': required_docs,
            'recommendations': recommendations,
            'assessed_at': datetime.now().isoformat()
        }

    def collect_policies(self, output_dir: Path):
        """Collecte les politiques pour l'audit"""
        output_dir.mkdir(parents=True, exist_ok=True)

        # TODO: Copier les politiques générées
        # Pour l'instant, créer un fichier index
        index_content = "# Politiques de sécurité de l'information\n\n"
        index_content += f"*Collecté le {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
        index_content += "Les politiques suivantes doivent être placées dans ce répertoire:\n\n"

        policies = [
            'information_security_policy.md',
            'access_control_policy.md',
            'asset_management_policy.md',
            'incident_management_policy.md',
        ]

        for policy in policies:
            index_content += f"- [ ] {policy}\n"

        (output_dir / 'README.md').write_text(index_content, encoding='utf-8')

    def collect_controls_evidence(self, output_dir: Path):
        """Collecte les preuves d'implémentation des contrôles"""
        output_dir.mkdir(parents=True, exist_ok=True)

        all_controls = get_all_controls()
        content = "# Preuves d'implémentation des contrôles\n\n"
        content += f"*Généré le {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"

        for control in all_controls:
            status = self.controls_tracker.get_control_status(control['id'])
            evidence = self.controls_tracker.get_control_evidence(control['id'])
            notes = self.controls_tracker.get_control_notes(control['id'])

            if status in ['implemented', 'verified']:
                content += f"## {control['id']} - {control['name']}\n\n"
                content += f"**Statut:** {status}\n\n"

                if notes:
                    content += f"**Notes:**\n{notes}\n\n"

                if evidence:
                    content += f"**Preuves:**\n"
                    for ev in evidence:
                        content += f"- {ev}\n"
                    content += "\n"

        (output_dir / 'controls_evidence.md').write_text(content, encoding='utf-8')

    def collect_risk_evidence(self, output_dir: Path):
        """Collecte les preuves de gestion des risques"""
        output_dir.mkdir(parents=True, exist_ok=True)

        risks = self.risk_manager.get_all_risks()

        content = "# Registre des risques\n\n"
        content += f"*Généré le {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"

        for risk in risks:
            content += f"## {risk['id']} - {risk['name']}\n\n"
            content += f"- **Catégorie:** {risk['category']}\n"
            content += f"- **Impact:** {risk['impact']}/5\n"
            content += f"- **Probabilité:** {risk['likelihood']}/5\n"
            content += f"- **Niveau:** {risk['risk_level']}\n"
            content += f"- **Traitement:** {risk['treatment']}\n"
            content += f"- **Statut:** {risk['status']}\n\n"

            if risk.get('mitigation_measures'):
                content += "**Mesures de traitement:**\n"
                for measure in risk['mitigation_measures']:
                    content += f"- {measure}\n"
                content += "\n"

        (output_dir / 'risk_register.md').write_text(content, encoding='utf-8')

    def generate_summary_reports(self, output_dir: Path):
        """Génère des rapports de synthèse"""
        output_dir.mkdir(parents=True, exist_ok=True)

        # Rapport de synthèse
        readiness = self.assess_readiness()

        content = "# Rapport de préparation à l'audit ISO 27001\n\n"
        content += f"*Généré le {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
        content += f"## Score de préparation: {readiness['overall_score']}%\n\n"

        content += "## Statut des contrôles\n\n"
        stats = readiness['controls_status']
        content += f"- **Total:** {stats['total']}\n"
        content += f"- **Vérifiés:** {stats.get('verified', 0)}\n"
        content += f"- **Implémentés:** {stats.get('implemented', 0)}\n"
        content += f"- **En cours:** {stats.get('in_progress', 0)}\n"
        content += f"- **Non démarrés:** {stats.get('not_started', 0)}\n\n"

        if readiness['recommendations']:
            content += "## Recommandations\n\n"
            for rec in readiness['recommendations']:
                content += f"- {rec}\n"

        (output_dir / 'readiness_summary.md').write_text(content, encoding='utf-8')

    def perform_gap_analysis(self) -> Dict:
        """Effectue une analyse des écarts"""
        all_controls = get_all_controls()

        gaps = {
            'critical_gaps': [],
            'major_gaps': [],
            'minor_gaps': [],
            'by_category': {}
        }

        for control in all_controls:
            status = self.controls_tracker.get_control_status(control['id'])
            category = control['category']

            if category not in gaps['by_category']:
                gaps['by_category'][category] = {
                    'name': control['category_name'],
                    'critical': 0,
                    'major': 0,
                    'minor': 0
                }

            if status == 'not_started':
                gap = {
                    'control_id': control['id'],
                    'name': control['name'],
                    'category': category,
                    'severity': 'critical'
                }
                gaps['critical_gaps'].append(gap)
                gaps['by_category'][category]['critical'] += 1

            elif status == 'in_progress':
                gap = {
                    'control_id': control['id'],
                    'name': control['name'],
                    'category': category,
                    'severity': 'major'
                }
                gaps['major_gaps'].append(gap)
                gaps['by_category'][category]['major'] += 1

        return gaps

    def schedule_audit(self, audit_info: Dict):
        """Planifie un audit"""
        self.data['audits'].append(audit_info)
        self.save()

    def generate_soa(self) -> Dict:
        """Génère la Déclaration d'Applicabilité (Statement of Applicability)"""
        all_controls = get_all_controls()

        soa = {
            'generated_at': datetime.now().isoformat(),
            'total_controls': len(all_controls),
            'applicable_controls': 0,
            'implemented_controls': 0,
            'controls': []
        }

        for control in all_controls:
            status = self.controls_tracker.get_control_status(control['id'])
            notes = self.controls_tracker.get_control_notes(control['id'])

            # Pour cet exemple, tous les contrôles sont considérés comme applicables
            applicable = True
            soa['applicable_controls'] += 1

            if status in ['implemented', 'verified']:
                soa['implemented_controls'] += 1

            soa['controls'].append({
                'id': control['id'],
                'name': control['name'],
                'category': control['category'],
                'applicable': applicable,
                'status': status,
                'justification': notes or 'Contrôle applicable pour la protection des actifs de l\'organisation',
                'implementation_notes': notes
            })

        return soa
