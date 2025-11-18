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


@main.command()
def doctor():
    """Diagnostic de santé du projet ISO 27001"""
    import os
    import stat
    import yaml
    from pathlib import Path
    from iso27001_toolkit.utils.config import CONFIG_DIR, get_data_dir
    from iso27001_toolkit.utils.risk_manager import RiskManager
    from iso27001_toolkit.utils.controls_tracker import ControlsTracker
    from iso27001_toolkit.utils.audit_helper import AuditHelper

    console = Console()

    issues = []
    warnings = []
    ok_checks = []

    console.print("\n[bold cyan]🩺 ISO 27001 Doctor - Diagnostic de santé[/bold cyan]\n")
    console.print("Analyse en cours...\n")

    # Check 1: Répertoire de configuration
    console.print("[dim]Vérification du répertoire de configuration...[/dim]")
    if CONFIG_DIR.exists():
        ok_checks.append(f"✓ Répertoire de configuration existe: {CONFIG_DIR}")

        # Vérifier les permissions
        perms = stat.S_IMODE(os.stat(CONFIG_DIR).st_mode)
        if perms & stat.S_IRWXO:  # World-readable
            warnings.append(f"⚠️  Le répertoire {CONFIG_DIR} est accessible par d'autres utilisateurs (permissions: {oct(perms)})")
        else:
            ok_checks.append(f"✓ Permissions du répertoire sont restrictives")
    else:
        issues.append(f"✗ Répertoire de configuration n'existe pas: {CONFIG_DIR}")
        console.print("\n[red]Le projet n'est pas initialisé. Exécutez:[/red]")
        console.print("[cyan]iso27001 init[/cyan]\n")
        return

    # Check 2: Fichiers de données
    console.print("[dim]Vérification des fichiers de données...[/dim]")
    data_dir = get_data_dir()

    expected_files = {
        'controls.yml': 'Fichier de suivi des contrôles',
        'risks.yml': 'Fichier de gestion des risques',
        'audit.yml': 'Fichier de préparation d\'audit'
    }

    for filename, description in expected_files.items():
        filepath = data_dir / filename
        if filepath.exists():
            ok_checks.append(f"✓ {description} existe")

            # Vérifier la validité YAML
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    yaml.safe_load(f)
                ok_checks.append(f"✓ {description} est un YAML valide")
            except yaml.YAMLError as e:
                issues.append(f"✗ {description} est corrompu: {e}")
            except Exception as e:
                issues.append(f"✗ Erreur de lecture {description}: {e}")

            # Vérifier les permissions
            perms = stat.S_IMODE(os.stat(filepath).st_mode)
            if perms & stat.S_IRWXO:  # World-readable/writable
                warnings.append(f"⚠️  {description} est accessible par d'autres utilisateurs")
        else:
            warnings.append(f"⚠️  {description} n'existe pas")

    # Check 3: Audit trail
    console.print("[dim]Vérification de l'audit trail...[/dim]")
    audit_file = CONFIG_DIR / "audit_trail.yml"
    if audit_file.exists():
        ok_checks.append(f"✓ Audit trail existe")

        # Vérifier permissions strictes (0600)
        perms = stat.S_IMODE(os.stat(audit_file).st_mode)
        if perms == 0o600:
            ok_checks.append(f"✓ Audit trail a des permissions sécurisées (0600)")
        else:
            warnings.append(f"⚠️  Audit trail devrait avoir permissions 0600, actuellement {oct(perms)}")

        # Vérifier validité
        try:
            with open(audit_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            if 'audit_trail' in data:
                entries_count = len(data['audit_trail'])
                ok_checks.append(f"✓ Audit trail contient {entries_count} entrées")
        except:
            issues.append(f"✗ Audit trail est corrompu")
    else:
        warnings.append(f"⚠️  Audit trail n'existe pas encore")

    # Check 4: Clé de chiffrement
    console.print("[dim]Vérification de la clé de chiffrement...[/dim]")
    encryption_key = CONFIG_DIR / "encryption.key"
    if encryption_key.exists():
        ok_checks.append(f"✓ Clé de chiffrement existe")

        # Vérifier permissions (doit être 0600)
        perms = stat.S_IMODE(os.stat(encryption_key).st_mode)
        if perms == 0o600:
            ok_checks.append(f"✓ Clé de chiffrement a des permissions sécurisées (0600)")
        else:
            issues.append(f"✗ CRITIQUE: Clé de chiffrement a des permissions non sécurisées ({oct(perms)}) - devrait être 0600")
    else:
        ok_checks.append(f"✓ Pas de clé de chiffrement (fonctionnalité non utilisée)")

    # Check 5: Intégrité des données
    console.print("[dim]Vérification de l'intégrité des données...[/dim]")
    try:
        # Tester RiskManager
        risk_manager = RiskManager()
        risks = risk_manager.get_all_risks()
        ok_checks.append(f"✓ RiskManager fonctionne ({len(risks)} risques)")

        # Vérifier cohérence des scores
        for risk in risks:
            if 'impact' in risk and 'likelihood' in risk:
                expected_score = risk['impact'] * risk['likelihood']
                if risk.get('risk_score') != expected_score:
                    warnings.append(f"⚠️  Risque {risk.get('id', '?')} a un score incohérent")

        # Tester ControlsTracker
        tracker = ControlsTracker()
        stats = tracker.get_statistics()
        if stats:
            ok_checks.append(f"✓ ControlsTracker fonctionne ({stats['total']} contrôles)")

        # Tester AuditHelper
        helper = AuditHelper()
        ok_checks.append(f"✓ AuditHelper fonctionne")

    except Exception as e:
        issues.append(f"✗ Erreur lors du test d'intégrité: {e}")

    # Check 6: Dépendances Python
    console.print("[dim]Vérification des dépendances...[/dim]")
    required_modules = ['click', 'jinja2', 'yaml', 'rich', 'tabulate', 'cryptography']
    for module in required_modules:
        try:
            __import__(module if module != 'yaml' else 'yaml')
            ok_checks.append(f"✓ Module {module} est installé")
        except ImportError:
            issues.append(f"✗ Module {module} manquant")

    # Affichage des résultats
    console.print("\n" + "="*60 + "\n")

    if issues:
        console.print(Panel(
            "\n".join(issues),
            title="[red]❌ Problèmes critiques détectés[/red]",
            border_style="red"
        ))
        console.print()

    if warnings:
        console.print(Panel(
            "\n".join(warnings),
            title="[yellow]⚠️  Avertissements[/yellow]",
            border_style="yellow"
        ))
        console.print()

    if ok_checks:
        console.print(Panel(
            "\n".join(ok_checks[:10]) + (f"\n... et {len(ok_checks)-10} autres vérifications OK" if len(ok_checks) > 10 else ""),
            title="[green]✓ Vérifications réussies[/green]",
            border_style="green"
        ))
        console.print()

    # Résumé
    total_checks = len(ok_checks) + len(warnings) + len(issues)
    health_score = (len(ok_checks) / total_checks * 100) if total_checks > 0 else 0

    if health_score >= 90:
        health_emoji = "🌟"
        health_status = "Excellent"
        health_color = "green"
    elif health_score >= 75:
        health_emoji = "✅"
        health_status = "Bon"
        health_color = "green"
    elif health_score >= 50:
        health_emoji = "⚠️"
        health_status = "Acceptable"
        health_color = "yellow"
    else:
        health_emoji = "❌"
        health_status = "Critique"
        health_color = "red"

    console.print(Panel(
        f"{health_emoji} [bold]Score de santé: {health_score:.0f}%[/bold] ({health_status})\n\n"
        f"[green]✓ {len(ok_checks)} vérifications OK[/green]\n"
        f"[yellow]⚠️  {len(warnings)} avertissements[/yellow]\n"
        f"[red]✗ {len(issues)} problèmes critiques[/red]",
        title=f"[{health_color}]Résumé du diagnostic[/{health_color}]",
        border_style=health_color
    ))

    # Recommandations
    if issues or warnings:
        console.print("\n[bold cyan]📝 Actions recommandées:[/bold cyan]\n")
        if issues:
            console.print("1. [red]Corriger les problèmes critiques immédiatement[/red]")
        if warnings:
            console.print("2. [yellow]Examiner et résoudre les avertissements[/yellow]")
        if any("permissions" in w.lower() for w in warnings + issues):
            console.print("3. [cyan]Corriger les permissions:[/cyan]")
            console.print(f"   chmod 700 {CONFIG_DIR}")
            console.print(f"   chmod 600 {CONFIG_DIR}/*.key {CONFIG_DIR}/audit_trail.yml")
        console.print()


# Enregistrer les groupes de commandes
main.add_command(policies.policies)
main.add_command(controls.controls)
main.add_command(risks.risks)
main.add_command(audit.audit)

# Importer et enregistrer le groupe export (conditionnel si WeasyPrint disponible)
try:
    from iso27001_toolkit.commands import export
    main.add_command(export.export)
except ImportError:
    # WeasyPrint non disponible - la commande export ne sera pas accessible
    pass


if __name__ == "__main__":
    main()
