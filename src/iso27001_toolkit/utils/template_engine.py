"""
Moteur de templates pour générer les documents ISO 27001
"""

import jinja2
from pathlib import Path
from typing import Dict, Any
from datetime import datetime


class TemplateEngine:
    """Moteur de rendu des templates Jinja2"""

    def __init__(self):
        # Récupérer le répertoire des templates
        self.template_dir = Path(__file__).parent.parent / 'templates'
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.template_dir)),
            autoescape=jinja2.select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )

        # Ajouter des filtres personnalisés
        self.env.filters['date'] = self._format_date

    def _format_date(self, value, format='%Y-%m-%d'):
        """Filtre pour formater les dates"""
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value)
            except:
                return value
        if isinstance(value, datetime):
            return value.strftime(format)
        return value

    def render_policy(self, policy_name: str, context: Dict[str, Any]) -> str:
        """Rend une politique à partir d'un template"""
        template_path = f"policies/{policy_name}.md"

        try:
            template = self.env.get_template(template_path)
            return template.render(**context, current_date=datetime.now().strftime('%Y-%m-%d'))
        except jinja2.exceptions.TemplateNotFound:
            raise FileNotFoundError(f"Template non trouvé: {template_path}")

    def render_risk_report(self, context: Dict[str, Any]) -> str:
        """Rend un rapport d'évaluation des risques"""
        template_path = "risks/risk_assessment.md"

        try:
            template = self.env.get_template(template_path)
            return template.render(**context)
        except jinja2.exceptions.TemplateNotFound:
            # Si le template n'existe pas, générer un rapport simple
            return self._generate_simple_risk_report(context)

    def _generate_simple_risk_report(self, context: Dict[str, Any]) -> str:
        """Génère un rapport de risques simple si pas de template"""
        content = "# Rapport d'évaluation des risques\n\n"
        content += f"*Généré le {context['generation_date']}*\n\n"
        content += "## Statistiques\n\n"
        content += f"- **Total des risques:** {context['total_risks']}\n"
        content += f"- **Risques critiques:** {context['critical_risks']}\n"
        content += f"- **Risques élevés:** {context['high_risks']}\n"
        content += f"- **Risques moyens:** {context['medium_risks']}\n"
        content += f"- **Risques faibles:** {context['low_risks']}\n\n"

        content += "## Détail des risques\n\n"

        for risk in context['risks']:
            content += f"### {risk['id']} - {risk['name']}\n\n"
            content += f"- **Catégorie:** {risk['category']}\n"
            content += f"- **Description:** {risk['description']}\n"
            content += f"- **Niveau:** {risk['risk_level']}\n"
            content += f"- **Score:** {risk['risk_score']}/25\n"
            content += f"- **Traitement:** {risk['treatment']}\n\n"

        return content

    def render_audit_checklist(self, checklist_data: Dict[str, Any]) -> str:
        """Rend une checklist d'audit"""
        template_path = "audit/checklist.md"

        try:
            template = self.env.get_template(template_path)
            return template.render(**checklist_data)
        except jinja2.exceptions.TemplateNotFound:
            return self._generate_simple_checklist(checklist_data)

    def _generate_simple_checklist(self, checklist_data: Dict[str, Any]) -> str:
        """Génère une checklist simple"""
        content = "# Checklist d'audit ISO 27001\n\n"
        content += f"*Généré le {checklist_data['generated_at']}*\n\n"

        for cat_id, cat_data in checklist_data.get('categories', {}).items():
            content += f"## {cat_id} - {cat_data['name']}\n\n"

            for control in cat_data['controls']:
                content += f"### {control['id']} - {control['name']}\n\n"
                content += f"**Statut:** {control['status']}\n\n"
                content += "**Points de vérification:**\n"

                for item in control['check_items']:
                    content += f"- [ ] {item}\n"

                content += "\n"

        return content

    def render_gap_analysis(self, gaps: Dict[str, Any]) -> str:
        """Rend une analyse des écarts"""
        content = "# Analyse des écarts ISO 27001\n\n"
        content += f"*Généré le {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"

        content += "## Résumé\n\n"
        content += f"- **Écarts critiques:** {len(gaps['critical_gaps'])}\n"
        content += f"- **Écarts majeurs:** {len(gaps['major_gaps'])}\n"
        content += f"- **Écarts mineurs:** {len(gaps['minor_gaps'])}\n\n"

        if gaps['critical_gaps']:
            content += "## Écarts critiques (contrôles non démarrés)\n\n"
            for gap in gaps['critical_gaps']:
                content += f"- **{gap['control_id']}** - {gap['name']}\n"
            content += "\n"

        if gaps['major_gaps']:
            content += "## Écarts majeurs (contrôles en cours)\n\n"
            for gap in gaps['major_gaps']:
                content += f"- **{gap['control_id']}** - {gap['name']}\n"
            content += "\n"

        content += "## Détail par catégorie\n\n"
        for cat_id, cat_data in gaps['by_category'].items():
            content += f"### {cat_id} - {cat_data['name']}\n\n"
            content += f"- Écarts critiques: {cat_data['critical']}\n"
            content += f"- Écarts majeurs: {cat_data['major']}\n"
            content += f"- Écarts mineurs: {cat_data['minor']}\n\n"

        return content

    def render_soa(self, soa_data: Dict[str, Any]) -> str:
        """Rend la Déclaration d'Applicabilité"""
        content = "# Déclaration d'Applicabilité (Statement of Applicability)\n\n"
        content += f"*Généré le {soa_data['generated_at']}*\n\n"

        content += "## Résumé\n\n"
        content += f"- **Total des contrôles ISO 27001:2022:** {soa_data['total_controls']}\n"
        content += f"- **Contrôles applicables:** {soa_data['applicable_controls']}\n"
        content += f"- **Contrôles implémentés:** {soa_data['implemented_controls']}\n\n"

        # Grouper par catégorie
        categories = {}
        for control in soa_data['controls']:
            cat = control['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(control)

        content += "## Détail des contrôles\n\n"

        for cat_id, controls in sorted(categories.items()):
            cat_name = controls[0].get('name', '') if controls else cat_id
            content += f"### {cat_id}\n\n"
            content += "| ID | Nom | Applicable | Statut | Justification |\n"
            content += "|----|-----|-----------|--------|---------------|\n"

            for control in controls:
                applicable = "Oui" if control['applicable'] else "Non"
                content += f"| {control['id']} | {control['name']} | {applicable} | {control['status']} | {control['justification'][:50]}... |\n"

            content += "\n"

        return content
