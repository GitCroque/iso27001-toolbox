#!/usr/bin/env python3
"""
CLI principal pour ISO 27001 Toolkit
"""

import click
from rich.console import Console
from rich.panel import Panel

from iso27001_toolkit.commands import policies, controls, risks, audit, export, import_data
from iso27001_toolkit.utils.controls_data import get_all_controls
from rich.table import Table

console = Console()


@click.group()
@click.version_option(version="0.2.0")
def main():
    """
    ISO 27001 Toolkit - Suite d'outils pour gérer votre certification ISO 27001

    Outils disponibles:
    - Génération de politiques de sécurité
    - Suivi des contrôles de sécurité
    - Gestion des risques
    - Préparation d'audits
    - Export/Import de données
    """
    pass


@main.command()
def info():
    """Affiche les informations sur l'outil"""
    console.print(Panel.fit(
        "[bold cyan]ISO 27001 Toolkit v0.2.0[/bold cyan]\n\n"
        "Suite d'outils CLI pour faciliter votre démarche de certification ISO 27001\n\n"
        "[yellow]Fonctionnalités:[/yellow]\n"
        "• Génération de politiques de sécurité personnalisées\n"
        "• Suivi des 114 contrôles ISO 27001:2022 (Annexe A)\n"
        "• Gestion complète des risques (identification, analyse, traitement)\n"
        "• Préparation d'audits avec checklist et rapports\n"
        "• Export/Import de données (JSON, CSV)\n"
        "• Recherche dans les contrôles\n\n"
        "[green]Utilisation:[/green] iso27001 --help",
        title="📋 ISO 27001 Toolkit",
        border_style="cyan"
    ))


@main.command()
@click.argument('query')
@click.option('--in-description', '-d', is_flag=True, help='Rechercher aussi dans les descriptions')
def search(query, in_description):
    """Recherche dans les contrôles ISO 27001"""
    console.print(f"[bold cyan]Recherche: '{query}'[/bold cyan]\n")

    all_controls = get_all_controls()
    results = []

    query_lower = query.lower()

    for control in all_controls:
        # Recherche dans l'ID et le nom
        if (query_lower in control['id'].lower() or
            query_lower in control['name'].lower()):
            results.append(control)
        # Recherche dans la description si demandé
        elif in_description and query_lower in control['description'].lower():
            results.append(control)

    if not results:
        console.print(f"[yellow]Aucun résultat trouvé pour '{query}'[/yellow]")
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("ID", style="cyan", width=8)
    table.add_column("Nom", width=50)
    table.add_column("Catégorie", width=15)

    for control in results:
        table.add_row(
            control['id'],
            control['name'][:47] + "..." if len(control['name']) > 50 else control['name'],
            control['category_name']
        )

    console.print(table)
    console.print(f"\n[bold green]{len(results)} résultat(s) trouvé(s)[/bold green]")


# Enregistrer les groupes de commandes
main.add_command(policies.policies)
main.add_command(controls.controls)
main.add_command(risks.risks)
main.add_command(audit.audit)
main.add_command(export.export)
main.add_command(import_data.import_cmd)


if __name__ == "__main__":
    main()
