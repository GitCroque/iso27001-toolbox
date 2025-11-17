#!/usr/bin/env python3
"""
CLI principal pour ISO 27001 Toolkit
"""

import click
from rich.console import Console
from rich.panel import Panel

from iso27001_toolkit.commands import policies, controls, risks, audit

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def main():
    """
    ISO 27001 Toolkit - Suite d'outils pour gérer votre certification ISO 27001

    Outils disponibles:
    - Génération de politiques de sécurité
    - Suivi des contrôles de sécurité
    - Gestion des risques
    - Préparation d'audits
    """
    pass


@main.command()
def info():
    """Affiche les informations sur l'outil"""
    console.print(Panel.fit(
        "[bold cyan]ISO 27001 Toolkit[/bold cyan]\n\n"
        "Suite d'outils CLI pour faciliter votre démarche de certification ISO 27001\n\n"
        "[yellow]Fonctionnalités:[/yellow]\n"
        "• Génération de politiques de sécurité personnalisées\n"
        "• Suivi des 114 contrôles ISO 27001:2022 (Annexe A)\n"
        "• Gestion complète des risques (identification, analyse, traitement)\n"
        "• Préparation d'audits avec checklist et rapports\n\n"
        "[green]Utilisation:[/green] iso27001 --help",
        title="📋 ISO 27001 Toolkit",
        border_style="cyan"
    ))


# Enregistrer les groupes de commandes
main.add_command(policies.policies)
main.add_command(controls.controls)
main.add_command(risks.risks)
main.add_command(audit.audit)


if __name__ == "__main__":
    main()
