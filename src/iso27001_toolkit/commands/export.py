"""
Commandes d'export (PDF, CSV, JSON)
"""

import click
import json
import csv
from pathlib import Path
from rich.console import Console
from datetime import datetime

from iso27001_toolkit.utils.controls_tracker import ControlsTracker
from iso27001_toolkit.utils.risk_manager import RiskManager
from iso27001_toolkit.utils.controls_data import get_all_controls

console = Console()


@click.group()
def export():
    """Export de données vers différents formats"""
    pass


@export.command()
@click.option('--format', '-f', type=click.Choice(['json', 'csv']), default='json', help='Format d\'export')
@click.option('--output', '-o', help='Fichier de sortie')
def controls(format, output):
    """Exporte l'état des contrôles"""
    console.print("[bold cyan]Export des contrôles...[/bold cyan]")

    tracker = ControlsTracker()
    all_controls = get_all_controls()

    # Préparer les données
    export_data = []
    for control in all_controls:
        status = tracker.get_control_status(control['id'])
        priority = tracker.get_control_priority(control['id'])
        notes = tracker.get_control_notes(control['id'])
        evidence = tracker.get_control_evidence(control['id'])

        export_data.append({
            'id': control['id'],
            'name': control['name'],
            'category': control['category'],
            'category_name': control['category_name'],
            'type': control['type'],
            'status': status,
            'priority': priority,
            'notes': notes,
            'evidence_count': len(evidence),
            'evidence': evidence
        })

    # Générer le fichier de sortie
    if not output:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output = f'controls_export_{timestamp}.{format}'

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if format == 'json':
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
    elif format == 'csv':
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            if export_data:
                writer = csv.DictWriter(f, fieldnames=export_data[0].keys())
                writer.writeheader()
                for row in export_data:
                    # Convertir les listes en chaînes pour CSV
                    row['evidence'] = '; '.join(row['evidence']) if row['evidence'] else ''
                    writer.writerow(row)

    console.print(f"[bold green]✓ Export réussi: {output_path.absolute()}[/bold green]")


@export.command()
@click.option('--format', '-f', type=click.Choice(['json', 'csv']), default='json')
@click.option('--output', '-o', help='Fichier de sortie')
def risks(format, output):
    """Exporte les risques"""
    console.print("[bold cyan]Export des risques...[/bold cyan]")

    manager = RiskManager()
    risks_data = manager.get_all_risks()

    if not output:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output = f'risks_export_{timestamp}.{format}'

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if format == 'json':
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(risks_data, f, ensure_ascii=False, indent=2)
    elif format == 'csv':
        if risks_data:
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                # Flatten les listes pour CSV
                flattened = []
                for risk in risks_data:
                    flat_risk = risk.copy()
                    flat_risk['assets'] = '; '.join(risk.get('assets', []))
                    flat_risk['mitigation_measures'] = '; '.join(risk.get('mitigation_measures', []))
                    flat_risk['controls'] = '; '.join(risk.get('controls', []))
                    flattened.append(flat_risk)

                writer = csv.DictWriter(f, fieldnames=flattened[0].keys())
                writer.writeheader()
                writer.writerows(flattened)

    console.print(f"[bold green]✓ Export réussi: {output_path.absolute()}[/bold green]")


@export.command()
@click.option('--output', '-o', default='full_export.json', help='Fichier de sortie')
def full(output):
    """Exporte toutes les données (contrôles + risques)"""
    console.print("[bold cyan]Export complet...[/bold cyan]")

    tracker = ControlsTracker()
    manager = RiskManager()

    export_data = {
        'export_date': datetime.now().isoformat(),
        'organization': 'ISO 27001 Toolkit Export',
        'controls': tracker.data,
        'risks': manager.data
    }

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)

    console.print(f"[bold green]✓ Export complet réussi: {output_path.absolute()}[/bold green]")
