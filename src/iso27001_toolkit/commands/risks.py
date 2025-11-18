"""
Commandes pour la gestion des risques ISO 27001
"""

import click
import yaml
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm, IntPrompt
from datetime import datetime

from iso27001_toolkit.utils.risk_manager import RiskManager
from iso27001_toolkit.utils.template_engine import TemplateEngine
from iso27001_toolkit.constants import (
    RISK_SCORE_MIN, RISK_SCORE_MAX,
    RISK_COLOR_MAP, RISK_STATUS_COLOR_MAP
)

console = Console()


@click.group()
def risks():
    """Gestion des risques de sécurité de l'information"""
    pass


@risks.command()
@click.option('--category', '-c', help='Filtrer par catégorie')
@click.option('--level', '-l', type=click.Choice(['low', 'medium', 'high', 'critical']), help='Filtrer par niveau de risque')
@click.option('--status', '-s', type=click.Choice(['identified', 'analyzed', 'treated', 'accepted', 'monitoring']), help='Filtrer par statut')
def list(category, level, status):
    """Liste tous les risques identifiés"""
    manager = RiskManager()
    risks = manager.get_all_risks()

    # Filtrer les risques
    if category:
        risks = [r for r in risks if r.get('category') == category]
    if level:
        risks = [r for r in risks if r.get('risk_level') == level]
    if status:
        risks = [r for r in risks if r.get('status') == status]

    if not risks:
        console.print("[yellow]Aucun risque trouvé[/yellow]")
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("ID", style="cyan", width=8)
    table.add_column("Nom du risque", width=30)
    table.add_column("Catégorie", width=15)
    table.add_column("Niveau", width=10)
    table.add_column("Statut", width=12)
    table.add_column("Traitement", width=15)

    for risk in risks:
        level_color = RISK_COLOR_MAP.get(risk.get('risk_level', 'medium'), 'white')
        status_color = RISK_STATUS_COLOR_MAP.get(risk.get('status', 'identified'), 'white')

        table.add_row(
            risk.get('id', 'N/A'),
            risk.get('name', 'Sans nom')[:27] + "..." if len(risk.get('name', '')) > 30 else risk.get('name', 'Sans nom'),
            risk.get('category', 'N/A'),
            f"[{level_color}]{risk.get('risk_level', 'N/A')}[/{level_color}]",
            f"[{status_color}]{risk.get('status', 'N/A')}[/{status_color}]",
            risk.get('treatment', 'N/A')
        )

    console.print(f"\n[bold cyan]Registre des risques[/bold cyan] ({len(risks)} risques)\n")
    console.print(table)

    # Afficher les statistiques
    stats = {
        'low': 0, 'medium': 0, 'high': 0, 'critical': 0
    }
    for risk in risks:
        level = risk.get('risk_level', 'medium')
        stats[level] = stats.get(level, 0) + 1

    console.print(f"\n[yellow]Répartition:[/yellow] "
                  f"[green]Faible: {stats['low']}[/green] | "
                  f"[yellow]Moyen: {stats['medium']}[/yellow] | "
                  f"[red]Élevé: {stats['high']}[/red] | "
                  f"[bold red]Critique: {stats['critical']}[/bold red]")


@risks.command()
@click.argument('risk_id')
def show(risk_id):
    """Affiche les détails d'un risque"""
    manager = RiskManager()
    risk = manager.get_risk(risk_id.upper())

    if not risk:
        console.print(f"[red]✗[/red] Risque {risk_id} non trouvé")
        return

    console.print(f"\n[bold cyan]Risque {risk['id']} - {risk['name']}[/bold cyan]\n")
    console.print(f"[yellow]Catégorie:[/yellow] {risk.get('category', 'N/A')}")
    console.print(f"[yellow]Description:[/yellow]\n{risk.get('description', 'N/A')}\n")

    console.print(f"[yellow]Actifs concernés:[/yellow] {', '.join(risk.get('assets', ['N/A']))}")
    console.print(f"\n[yellow]Analyse du risque:[/yellow]")
    console.print(f"  • Impact: {risk.get('impact', 'N/A')}/5")
    console.print(f"  • Probabilité: {risk.get('likelihood', 'N/A')}/5")
    console.print(f"  • Score: {risk.get('risk_score', 'N/A')}/25")
    console.print(f"  • Niveau: {risk.get('risk_level', 'N/A')}")

    console.print(f"\n[yellow]Statut:[/yellow] {risk.get('status', 'N/A')}")
    console.print(f"[yellow]Traitement:[/yellow] {risk.get('treatment', 'N/A')}")

    if risk.get('mitigation_measures'):
        console.print(f"\n[yellow]Mesures de traitement:[/yellow]")
        for measure in risk['mitigation_measures']:
            console.print(f"  • {measure}")

    if risk.get('controls'):
        console.print(f"\n[yellow]Contrôles associés:[/yellow] {', '.join(risk['controls'])}")

    if risk.get('owner'):
        console.print(f"\n[yellow]Propriétaire:[/yellow] {risk['owner']}")

    if risk.get('review_date'):
        console.print(f"[yellow]Prochaine revue:[/yellow] {risk['review_date']}")


@risks.command()
@click.option('--interactive', '-i', is_flag=True, help='Mode interactif')
def add(interactive):
    """Ajoute un nouveau risque"""
    manager = RiskManager()

    if interactive:
        console.print("[bold cyan]Ajout d'un nouveau risque[/bold cyan]\n")

        name = Prompt.ask("Nom du risque")
        description = Prompt.ask("Description")
        category = Prompt.ask("Catégorie", choices=[
            'confidentiality', 'integrity', 'availability',
            'compliance', 'operational', 'strategic', 'financial'
        ])

        assets = Prompt.ask("Actifs concernés (séparés par des virgules)").split(',')
        assets = [a.strip() for a in assets]

        console.print("\n[yellow]Analyse du risque (échelle 1-5):[/yellow]")
        impact = IntPrompt.ask("Impact", default=3)
        likelihood = IntPrompt.ask("Probabilité", default=3)

        treatment = Prompt.ask("Type de traitement", choices=[
            'mitigate', 'accept', 'transfer', 'avoid'
        ], default='mitigate')

        mitigation = []
        console.print("\n[yellow]Mesures de traitement (vide pour terminer):[/yellow]")
        while True:
            measure = Prompt.ask("Mesure", default="")
            if not measure:
                break
            mitigation.append(measure)

        owner = Prompt.ask("Propriétaire du risque", default="")

        risk_data = {
            'name': name,
            'description': description,
            'category': category,
            'assets': assets,
            'impact': impact,
            'likelihood': likelihood,
            'treatment': treatment,
            'mitigation_measures': mitigation,
            'owner': owner
        }

        risk_id = manager.add_risk(risk_data)
        console.print(f"\n[bold green]✓ Risque {risk_id} ajouté avec succès[/bold green]")
    else:
        console.print("[yellow]Utilisez --interactive pour ajouter un risque en mode interactif[/yellow]")


@risks.command()
@click.argument('risk_id')
@click.option('--status', '-s', type=click.Choice(['identified', 'analyzed', 'treated', 'accepted', 'monitoring']))
@click.option('--treatment', '-t', type=click.Choice(['mitigate', 'accept', 'transfer', 'avoid']))
@click.option('--impact', '-i', type=int)
@click.option('--likelihood', '-l', type=int)
def update(risk_id, status, treatment, impact, likelihood):
    """Met à jour un risque existant"""
    manager = RiskManager()
    risk = manager.get_risk(risk_id.upper())

    if not risk:
        console.print(f"[red]✗[/red] Risque {risk_id} non trouvé")
        return

    updates = {}
    if status:
        updates['status'] = status
    if treatment:
        updates['treatment'] = treatment
    if impact is not None:
        updates['impact'] = impact
    if likelihood is not None:
        updates['likelihood'] = likelihood

    if updates:
        manager.update_risk(risk_id.upper(), updates)
        console.print(f"[bold green]✓ Risque {risk_id} mis à jour[/bold green]")
    else:
        console.print("[yellow]Aucune mise à jour spécifiée[/yellow]")


@risks.command()
@click.option('--output', '-o', default='output/risk_assessment.md', help='Fichier de sortie')
@click.option('--format', '-f', type=click.Choice(['markdown', 'yaml']), default='markdown')
def report(output, format):
    """Génère un rapport d'évaluation des risques"""
    manager = RiskManager()
    engine = TemplateEngine()

    risks = manager.get_all_risks()

    if format == 'markdown':
        # Utiliser le template pour générer le rapport
        context = {
            'risks': risks,
            'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'total_risks': len(risks),
            'critical_risks': len([r for r in risks if r.get('risk_level') == 'critical']),
            'high_risks': len([r for r in risks if r.get('risk_level') == 'high']),
            'medium_risks': len([r for r in risks if r.get('risk_level') == 'medium']),
            'low_risks': len([r for r in risks if r.get('risk_level') == 'low']),
        }

        content = engine.render_risk_report(context)
    else:
        # Format YAML
        content = yaml.dump({'risks': risks}, allow_unicode=True, sort_keys=False)

    # Sauvegarder le rapport
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding='utf-8')

    console.print(f"\n[bold green]✓ Rapport généré avec succès[/bold green]")
    console.print(f"[dim]Emplacement: {output_path.absolute()}[/dim]")


@risks.command()
def init():
    """Initialise le registre des risques"""
    manager = RiskManager()
    manager.initialize()
    console.print("[bold green]✓ Registre des risques initialisé[/bold green]")


@risks.command()
def matrix():
    """Affiche la matrice des risques"""
    manager = RiskManager()
    risks = manager.get_all_risks()

    console.print("\n[bold cyan]Matrice des risques[/bold cyan]\n")

    # Créer une matrice 5x5
    matrix = [[[] for _ in range(5)] for _ in range(5)]

    for risk in risks:
        impact = risk.get('impact', 3) - 1
        likelihood = risk.get('likelihood', 3) - 1
        if 0 <= impact < 5 and 0 <= likelihood < 5:
            matrix[4 - likelihood][impact].append(risk['id'])

    # Afficher la matrice
    console.print("        Impact →")
    console.print("      1    2    3    4    5")
    console.print("    ┌────┬────┬────┬────┬────┐")

    likelihood_labels = ['5', '4', '3', '2', '1']
    for i, row in enumerate(matrix):
        if i == 0:
            console.print(f"  P {likelihood_labels[i]} │", end="")
        else:
            console.print(f"  r {likelihood_labels[i]} │", end="")

        for cell in row:
            cell_color = 'green'
            if i + max(matrix[0].index(cell) if cell in matrix[0] else 0, 0) >= 6:
                cell_color = 'red'
            elif i + max(matrix[0].index(cell) if cell in matrix[0] else 0, 0) >= 4:
                cell_color = 'yellow'

            if cell:
                console.print(f" [{cell_color}]{len(cell):2d}[/{cell_color}] ", end="")
            else:
                console.print("  · ", end="")
            console.print("│", end="")
        console.print()

    console.print("    └────┴────┴────┴────┴────┘")
    console.print("\n[green]Vert:[/green] Risque faible  [yellow]Jaune:[/yellow] Risque moyen  [red]Rouge:[/red] Risque élevé")
