"""
Commandes pour le suivi des contrôles ISO 27001 (Annexe A)
"""

import click
import yaml
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from datetime import datetime

from iso27001_toolkit.utils.controls_data import get_all_controls, get_control_by_id
from iso27001_toolkit.utils.controls_tracker import ControlsTracker

console = Console()


@click.group()
def controls():
    """Suivi des 114 contrôles ISO 27001:2022 (Annexe A)"""
    pass


@controls.command()
@click.option('--category', '-c', help='Filtrer par catégorie (ex: A.5, A.8)')
@click.option('--status', '-s', help='Filtrer par statut (not_started, in_progress, implemented, verified)')
@click.option('--format', '-f', type=click.Choice(['table', 'summary']), default='table')
def list(category, status, format):
    """Liste tous les contrôles ISO 27001"""
    all_controls = get_all_controls()
    tracker = ControlsTracker()

    # Filtrer les contrôles
    filtered_controls = all_controls
    if category:
        filtered_controls = [c for c in filtered_controls if c['id'].startswith(category)]

    if format == 'summary':
        # Afficher un résumé par catégorie
        categories = {}
        for control in all_controls:
            cat = control['category']
            if cat not in categories:
                categories[cat] = {'total': 0, 'implemented': 0}
            categories[cat]['total'] += 1
            control_status = tracker.get_control_status(control['id'])
            if control_status in ['implemented', 'verified']:
                categories[cat]['implemented'] += 1

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Catégorie", style="cyan")
        table.add_column("Description")
        table.add_column("Total", justify="right")
        table.add_column("Implémentés", justify="right", style="green")
        table.add_column("Progression", justify="right")

        for cat_id, cat_data in categories.items():
            cat_name = all_controls[0]['category_name'] if cat_id == all_controls[0]['category'] else cat_id
            for control in all_controls:
                if control['category'] == cat_id:
                    cat_name = control['category_name']
                    break

            progress = (cat_data['implemented'] / cat_data['total'] * 100) if cat_data['total'] > 0 else 0
            table.add_row(
                cat_id,
                cat_name,
                str(cat_data['total']),
                str(cat_data['implemented']),
                f"{progress:.1f}%"
            )

        console.print("\n[bold cyan]Résumé des contrôles ISO 27001:2022[/bold cyan]\n")
        console.print(table)
    else:
        # Afficher la liste détaillée
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("ID", style="cyan", width=8)
        table.add_column("Nom du contrôle", width=40)
        table.add_column("Statut", width=15)
        table.add_column("Priorité", width=10)

        for control in filtered_controls:
            control_status = tracker.get_control_status(control['id'])
            if status and control_status != status:
                continue

            status_color = {
                'not_started': 'red',
                'in_progress': 'yellow',
                'implemented': 'green',
                'verified': 'bold green'
            }.get(control_status, 'white')

            priority = tracker.get_control_priority(control['id'])
            priority_color = {
                'high': 'red',
                'medium': 'yellow',
                'low': 'green'
            }.get(priority, 'white')

            table.add_row(
                control['id'],
                control['name'][:37] + "..." if len(control['name']) > 40 else control['name'],
                f"[{status_color}]{control_status}[/{status_color}]",
                f"[{priority_color}]{priority}[/{priority_color}]"
            )

        console.print(f"\n[bold cyan]Contrôles ISO 27001:2022[/bold cyan] ({len(filtered_controls)} contrôles)\n")
        console.print(table)


@controls.command()
@click.argument('control_id')
def show(control_id):
    """Affiche les détails d'un contrôle spécifique"""
    control = get_control_by_id(control_id.upper())
    if not control:
        console.print(f"[red]✗[/red] Contrôle {control_id} non trouvé")
        return

    tracker = ControlsTracker()
    status = tracker.get_control_status(control_id)
    priority = tracker.get_control_priority(control_id)
    notes = tracker.get_control_notes(control_id)
    evidence = tracker.get_control_evidence(control_id)

    console.print(f"\n[bold cyan]{control['id']} - {control['name']}[/bold cyan]\n")
    console.print(f"[yellow]Catégorie:[/yellow] {control['category']} - {control['category_name']}")
    console.print(f"[yellow]Type:[/yellow] {control['type']}")
    console.print(f"\n[yellow]Description:[/yellow]\n{control['description']}\n")
    console.print(f"[yellow]Objectif:[/yellow]\n{control['purpose']}\n")

    status_color = {
        'not_started': 'red',
        'in_progress': 'yellow',
        'implemented': 'green',
        'verified': 'bold green'
    }.get(status, 'white')

    console.print(f"[yellow]Statut:[/yellow] [{status_color}]{status}[/{status_color}]")
    console.print(f"[yellow]Priorité:[/yellow] {priority}")

    if notes:
        console.print(f"\n[yellow]Notes:[/yellow]\n{notes}")

    if evidence:
        console.print(f"\n[yellow]Preuves:[/yellow]")
        for ev in evidence:
            console.print(f"  • {ev}")


@controls.command()
@click.argument('control_id')
@click.option('--status', '-s', type=click.Choice(['not_started', 'in_progress', 'implemented', 'verified']))
@click.option('--priority', '-p', type=click.Choice(['low', 'medium', 'high']))
@click.option('--notes', '-n', help='Notes sur l\'implémentation')
@click.option('--evidence', '-e', multiple=True, help='Preuves d\'implémentation')
def update(control_id, status, priority, notes, evidence):
    """Met à jour le statut d'un contrôle"""
    control = get_control_by_id(control_id.upper())
    if not control:
        console.print(f"[red]✗[/red] Contrôle {control_id} non trouvé")
        return

    tracker = ControlsTracker()

    if status:
        tracker.update_control_status(control_id.upper(), status)
        console.print(f"[green]✓[/green] Statut mis à jour: {status}")

    if priority:
        tracker.update_control_priority(control_id.upper(), priority)
        console.print(f"[green]✓[/green] Priorité mise à jour: {priority}")

    if notes:
        tracker.update_control_notes(control_id.upper(), notes)
        console.print(f"[green]✓[/green] Notes mises à jour")

    if evidence:
        tracker.add_control_evidence(control_id.upper(), list(evidence))
        console.print(f"[green]✓[/green] {len(evidence)} preuve(s) ajoutée(s)")

    tracker.save()


@controls.command()
@click.option('--output', '-o', default='output/controls_report.md', help='Fichier de sortie')
def report(output):
    """Génère un rapport sur l'état des contrôles"""
    all_controls = get_all_controls()
    tracker = ControlsTracker()

    # Calculer les statistiques
    stats = {
        'total': len(all_controls),
        'not_started': 0,
        'in_progress': 0,
        'implemented': 0,
        'verified': 0
    }

    for control in all_controls:
        status = tracker.get_control_status(control['id'])
        stats[status] = stats.get(status, 0) + 1

    progress = ((stats['implemented'] + stats['verified']) / stats['total'] * 100) if stats['total'] > 0 else 0

    # Générer le rapport
    report_content = f"""# Rapport d'implémentation ISO 27001:2022
*Généré le {datetime.now().strftime('%Y-%m-%d %H:%M')}*

## Statistiques globales

- **Total de contrôles:** {stats['total']}
- **Implémentés:** {stats['implemented'] + stats['verified']} ({progress:.1f}%)
- **En cours:** {stats['in_progress']}
- **Non démarrés:** {stats['not_started']}

## Progression par statut

| Statut | Nombre | Pourcentage |
|--------|--------|-------------|
| Vérifié | {stats['verified']} | {stats['verified']/stats['total']*100:.1f}% |
| Implémenté | {stats['implemented']} | {stats['implemented']/stats['total']*100:.1f}% |
| En cours | {stats['in_progress']} | {stats['in_progress']/stats['total']*100:.1f}% |
| Non démarré | {stats['not_started']} | {stats['not_started']/stats['total']*100:.1f}% |

## Détails par catégorie

"""

    # Grouper par catégorie
    categories = {}
    for control in all_controls:
        cat = control['category']
        if cat not in categories:
            categories[cat] = {
                'name': control['category_name'],
                'controls': []
            }
        categories[cat]['controls'].append(control)

    for cat_id, cat_data in sorted(categories.items()):
        report_content += f"\n### {cat_id} - {cat_data['name']}\n\n"
        report_content += "| ID | Nom | Statut | Priorité |\n"
        report_content += "|----|-----|--------|----------|\n"

        for control in cat_data['controls']:
            status = tracker.get_control_status(control['id'])
            priority = tracker.get_control_priority(control['id'])
            report_content += f"| {control['id']} | {control['name']} | {status} | {priority} |\n"

    # Sauvegarder le rapport
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_content, encoding='utf-8')

    console.print(f"\n[bold green]✓ Rapport généré avec succès[/bold green]")
    console.print(f"[dim]Emplacement: {output_path.absolute()}[/dim]")
    console.print(f"\nProgression globale: [cyan]{progress:.1f}%[/cyan]")


@controls.command()
def init():
    """Initialise le suivi des contrôles"""
    tracker = ControlsTracker()
    tracker.initialize()
    console.print("[bold green]✓ Suivi des contrôles initialisé[/bold green]")
