"""
Commandes d'import de données
"""

import click
import json
import csv
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm

from iso27001_toolkit.utils.controls_tracker import ControlsTracker
from iso27001_toolkit.utils.risk_manager import RiskManager

console = Console()


@click.group(name='import')
def import_cmd():
    """Import de données depuis différents formats"""
    pass


@import_cmd.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--merge', is_flag=True, help='Fusionner avec les données existantes')
def controls(file_path, merge):
    """Importe des contrôles depuis JSON/CSV"""
    console.print(f"[bold cyan]Import des contrôles depuis {file_path}...[/bold cyan]")

    path = Path(file_path)

    if not merge:
        if not Confirm.ask("⚠️  Ceci va écraser les données existantes. Continuer ?"):
            console.print("[yellow]Import annulé[/yellow]")
            return

    tracker = ControlsTracker()

    try:
        if path.suffix == '.json':
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'controls' in data:
                    tracker.data = data
                else:
                    console.print("[red]Format JSON invalide[/red]")
                    return

        elif path.suffix == '.csv':
            # TODO: Implémenter import CSV
            console.print("[yellow]Import CSV non encore implémenté[/yellow]")
            return

        tracker.save()
        console.print("[bold green]✓ Import réussi[/bold green]")

    except Exception as e:
        console.print(f"[red]✗ Erreur lors de l'import: {e}[/red]")


@import_cmd.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--merge', is_flag=True, help='Fusionner avec les données existantes')
def risks(file_path, merge):
    """Importe des risques depuis JSON/CSV"""
    console.print(f"[bold cyan]Import des risques depuis {file_path}...[/bold cyan]")

    path = Path(file_path)

    if not merge:
        if not Confirm.ask("⚠️  Ceci va écraser les données existantes. Continuer ?"):
            console.print("[yellow]Import annulé[/yellow]")
            return

    manager = RiskManager()

    try:
        if path.suffix == '.json':
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'risks' in data:
                    manager.data = data
                else:
                    console.print("[red]Format JSON invalide[/red]")
                    return

        elif path.suffix == '.csv':
            console.print("[yellow]Import CSV non encore implémenté[/yellow]")
            return

        manager.save()
        console.print("[bold green]✓ Import réussi[/bold green]")

    except Exception as e:
        console.print(f"[red]✗ Erreur lors de l'import: {e}[/red]")


@import_cmd.command()
@click.argument('file_path', type=click.Path(exists=True))
def full(file_path):
    """Importe toutes les données (contrôles + risques)"""
    console.print(f"[bold cyan]Import complet depuis {file_path}...[/bold cyan]")

    if not Confirm.ask("⚠️  Ceci va écraser TOUTES les données existantes. Continuer ?"):
        console.print("[yellow]Import annulé[/yellow]")
        return

    path = Path(file_path)

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if 'controls' in data and 'risks' in data:
            tracker = ControlsTracker()
            tracker.data = data['controls']
            tracker.save()

            manager = RiskManager()
            manager.data = data['risks']
            manager.save()

            console.print("[bold green]✓ Import complet réussi[/bold green]")
        else:
            console.print("[red]Format de fichier invalide[/red]")

    except Exception as e:
        console.print(f"[red]✗ Erreur lors de l'import: {e}[/red]")
