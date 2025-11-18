#!/usr/bin/env python3
"""
CLI principal pour ISO 27001 Toolkit
"""

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from iso27001_toolkit import __version__
from iso27001_toolkit.commands import policies, controls, risks, audit
from iso27001_toolkit.utils.controls_tracker import ControlsTracker
from iso27001_toolkit.utils.risk_manager import RiskManager
from iso27001_toolkit.utils.audit_helper import AuditHelper

console = Console()


@click.group()
@click.version_option(version=__version__)
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


@main.command()
def init():
    """Initialise un nouveau projet ISO 27001 (setup complet)"""
    console.print("\n[bold cyan]Initialisation du projet ISO 27001[/bold cyan]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:

        # 1. Initialiser les contrôles
        task1 = progress.add_task("Initialisation des 114 contrôles ISO 27001:2022...", total=None)
        tracker = ControlsTracker()
        tracker.initialize()
        progress.update(task1, completed=True)
        console.print("[green]✓[/green] 114 contrôles initialisés")

        # 2. Initialiser le registre des risques
        task2 = progress.add_task("Initialisation du registre des risques...", total=None)
        risk_manager = RiskManager()
        risk_manager.initialize()
        progress.update(task2, completed=True)
        console.print("[green]✓[/green] Registre des risques créé avec exemples")

        # 3. Préparer l'audit helper
        task3 = progress.add_task("Configuration de l'assistant d'audit...", total=None)
        audit_helper = AuditHelper()
        progress.update(task3, completed=True)
        console.print("[green]✓[/green] Assistant d'audit configuré")

    console.print("\n[bold green]Initialisation terminée avec succès ![/bold green]\n")

    console.print(Panel.fit(
        "[yellow]Prochaines étapes:[/yellow]\n\n"
        "1. Configurer votre organisation:\n"
        "   [cyan]iso27001 policies configure[/cyan]\n\n"
        "2. Consulter l'état actuel:\n"
        "   [cyan]iso27001 status[/cyan]\n\n"
        "3. Commencer l'implémentation:\n"
        "   [cyan]iso27001 controls list[/cyan]\n"
        "   [cyan]iso27001 controls update A.5.1 --status in_progress[/cyan]\n\n"
        "4. Gérer les risques:\n"
        "   [cyan]iso27001 risks add --interactive[/cyan]\n\n"
        "5. Évaluer votre préparation:\n"
        "   [cyan]iso27001 audit readiness[/cyan]",
        title="🚀 Démarrage Rapide",
        border_style="green"
    ))


@main.command()
def status():
    """Affiche le dashboard de l'état actuel du projet"""
    console.print("\n[bold cyan]Dashboard ISO 27001[/bold cyan]\n")

    try:
        # Charger les données
        tracker = ControlsTracker()
        risk_manager = RiskManager()
        audit_helper = AuditHelper()

        # 1. Statut des contrôles
        controls_stats = tracker.get_statistics()

        if controls_stats['total'] == 0:
            console.print("[yellow]⚠ Projet non initialisé. Exécutez:[/yellow] [cyan]iso27001 init[/cyan]\n")
            return

        controls_table = Table(title="📋 Statut des Contrôles", show_header=True, header_style="bold cyan")
        controls_table.add_column("Statut", style="cyan")
        controls_table.add_column("Nombre", justify="right")
        controls_table.add_column("Pourcentage", justify="right")

        total = controls_stats['total']

        statuses = [
            ('Vérifiés', 'verified', 'bold green'),
            ('Implémentés', 'implemented', 'green'),
            ('En cours', 'in_progress', 'yellow'),
            ('Non démarrés', 'not_started', 'red')
        ]

        for label, key, color in statuses:
            count = controls_stats.get(key, 0)
            percentage = (count / total * 100) if total > 0 else 0
            controls_table.add_row(
                f"[{color}]{label}[/{color}]",
                str(count),
                f"{percentage:.1f}%"
            )

        console.print(controls_table)
        console.print()

        # 2. Statut des risques
        risks = risk_manager.get_all_risks()
        risk_stats = risk_manager.get_statistics()

        risks_table = Table(title="⚠️  Registre des Risques", show_header=True, header_style="bold cyan")
        risks_table.add_column("Niveau", style="cyan")
        risks_table.add_column("Nombre", justify="right")

        risk_levels = [
            ('Critique', 'critical', 'bold red'),
            ('Élevé', 'high', 'red'),
            ('Moyen', 'medium', 'yellow'),
            ('Faible', 'low', 'green')
        ]

        for label, key, color in risk_levels:
            count = risk_stats['by_level'].get(key, 0)
            if count > 0:
                risks_table.add_row(f"[{color}]{label}[/{color}]", str(count))

        risks_table.add_row("[cyan]Total[/cyan]", f"[bold]{risk_stats['total']}[/bold]")

        console.print(risks_table)
        console.print()

        # 3. Score de préparation à l'audit
        readiness = audit_helper.assess_readiness()
        score = readiness['overall_score']

        # Déterminer couleur et niveau
        if score >= 90:
            score_color = "bold green"
            level = "Excellent"
            emoji = "🌟"
        elif score >= 75:
            score_color = "green"
            level = "Bon"
            emoji = "✅"
        elif score >= 60:
            score_color = "yellow"
            level = "Satisfaisant"
            emoji = "⚠️"
        else:
            score_color = "red"
            level = "Insuffisant"
            emoji = "❌"

        console.print(Panel.fit(
            f"[bold]Score de préparation:[/bold] [{score_color}]{score:.1f}%[/{score_color}]\n"
            f"[bold]Niveau:[/bold] {emoji} {level}",
            title="🎯 Préparation à l'Audit",
            border_style="cyan"
        ))

        # 4. Recommandations
        if readiness['recommendations']:
            console.print("\n[bold yellow]📌 Recommandations prioritaires:[/bold yellow]\n")
            for i, rec in enumerate(readiness['recommendations'][:5], 1):
                console.print(f"  {i}. {rec}")
            console.print()

        # 5. Actions rapides
        console.print(Panel.fit(
            "[yellow]Actions rapides:[/yellow]\n\n"
            "• Mettre à jour un contrôle: [cyan]iso27001 controls update <ID> --status implemented[/cyan]\n"
            "• Ajouter un risque: [cyan]iso27001 risks add --interactive[/cyan]\n"
            "• Générer un rapport: [cyan]iso27001 controls report[/cyan]\n"
            "• Analyser les écarts: [cyan]iso27001 audit gap-analysis[/cyan]",
            title="⚡ Actions",
            border_style="yellow"
        ))

    except Exception as e:
        console.print(f"[red]Erreur lors du chargement du dashboard: {e}[/red]")
        console.print("[yellow]Exécutez [cyan]iso27001 init[/cyan] pour initialiser le projet.[/yellow]")


# Enregistrer les groupes de commandes
main.add_command(policies.policies)
main.add_command(controls.controls)
main.add_command(risks.risks)
main.add_command(audit.audit)


if __name__ == "__main__":
    main()
