"""
Commandes pour la préparation d'audits ISO 27001
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from datetime import datetime

from iso27001_toolkit.utils.audit_helper import AuditHelper
from iso27001_toolkit.utils.template_engine import TemplateEngine
from iso27001_toolkit.utils.controls_tracker import ControlsTracker

console = Console()


@click.group()
def audit():
    """Préparation et suivi des audits ISO 27001"""
    pass


@audit.command()
@click.option('--output', '-o', default='output/audit_checklist.md', help='Fichier de sortie')
def checklist(output):
    """Génère une checklist complète pour l'audit"""
    console.print("[bold cyan]Génération de la checklist d'audit ISO 27001[/bold cyan]\n")

    helper = AuditHelper()
    engine = TemplateEngine()

    # Générer la checklist
    checklist_data = helper.generate_checklist()

    # Utiliser le template
    content = engine.render_audit_checklist(checklist_data)

    # Sauvegarder
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding='utf-8')

    console.print(f"[bold green]✓ Checklist générée avec succès[/bold green]")
    console.print(f"[dim]Emplacement: {output_path.absolute()}[/dim]")


@audit.command()
def readiness():
    """Évalue le niveau de préparation pour l'audit"""
    console.print("[bold cyan]Évaluation de la préparation à l'audit[/bold cyan]\n")

    helper = AuditHelper()
    tracker = ControlsTracker()

    # Analyser la préparation
    readiness_data = helper.assess_readiness()

    # Afficher les résultats
    console.print("[yellow]Documents requis:[/yellow]")
    for doc in readiness_data['required_documents']:
        status = "✓" if doc['exists'] else "✗"
        color = "green" if doc['exists'] else "red"
        console.print(f"  [{color}]{status}[/{color}] {doc['name']}")

    console.print(f"\n[yellow]Contrôles implémentés:[/yellow]")
    stats = readiness_data['controls_status']
    total = sum(stats.values())
    implemented = stats.get('implemented', 0) + stats.get('verified', 0)
    progress_pct = (implemented / total * 100) if total > 0 else 0

    console.print(f"  • Total: {total}")
    console.print(f"  • Implémentés: [green]{implemented}[/green] ({progress_pct:.1f}%)")
    console.print(f"  • En cours: [yellow]{stats.get('in_progress', 0)}[/yellow]")
    console.print(f"  • Non démarrés: [red]{stats.get('not_started', 0)}[/red]")

    # Score global
    overall_score = readiness_data['overall_score']
    score_color = 'red' if overall_score < 50 else 'yellow' if overall_score < 80 else 'green'

    console.print(f"\n[bold {score_color}]Score de préparation: {overall_score}%[/bold {score_color}]")

    if overall_score < 80:
        console.print("\n[yellow]Recommandations:[/yellow]")
        for rec in readiness_data['recommendations']:
            console.print(f"  • {rec}")


@audit.command()
@click.option('--output', '-o', default='output/evidence_package', help='Répertoire de sortie')
def prepare_evidence(output):
    """Prépare le package de preuves pour l'audit"""
    console.print("[bold cyan]Préparation du package de preuves[/bold cyan]\n")

    helper = AuditHelper()
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)

    with Progress() as progress:
        task = progress.add_task("[cyan]Collecte des preuves...", total=100)

        # Copier les documents
        progress.update(task, advance=20, description="[cyan]Copie des politiques...")
        helper.collect_policies(output_path / "01_policies")

        progress.update(task, advance=20, description="[cyan]Collecte des contrôles...")
        helper.collect_controls_evidence(output_path / "02_controls")

        progress.update(task, advance=20, description="[cyan]Collecte des risques...")
        helper.collect_risk_evidence(output_path / "03_risks")

        progress.update(task, advance=20, description="[cyan]Génération des rapports...")
        helper.generate_summary_reports(output_path / "04_reports")

        progress.update(task, advance=20, description="[cyan]Finalisation...")

    console.print(f"\n[bold green]✓ Package de preuves préparé[/bold green]")
    console.print(f"[dim]Emplacement: {output_path.absolute()}[/dim]")


@audit.command()
@click.option('--output', '-o', default='output/gap_analysis.md', help='Fichier de sortie')
def gap_analysis(output):
    """Effectue une analyse des écarts (gap analysis)"""
    console.print("[bold cyan]Analyse des écarts ISO 27001[/bold cyan]\n")

    helper = AuditHelper()
    engine = TemplateEngine()

    # Effectuer l'analyse
    gaps = helper.perform_gap_analysis()

    # Générer le rapport
    content = engine.render_gap_analysis(gaps)

    # Sauvegarder
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding='utf-8')

    # Afficher un résumé
    console.print("[yellow]Résumé des écarts:[/yellow]\n")

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Catégorie", style="cyan")
    table.add_column("Écarts critiques", justify="right", style="red")
    table.add_column("Écarts majeurs", justify="right", style="yellow")
    table.add_column("Écarts mineurs", justify="right", style="green")

    for category, data in gaps['by_category'].items():
        table.add_row(
            category,
            str(data.get('critical', 0)),
            str(data.get('major', 0)),
            str(data.get('minor', 0))
        )

    console.print(table)

    console.print(f"\n[bold green]✓ Analyse des écarts générée[/bold green]")
    console.print(f"[dim]Emplacement: {output_path.absolute()}[/dim]")


@audit.command()
@click.argument('audit_date')
@click.option('--auditor', '-a', help='Nom de l\'auditeur')
@click.option('--type', '-t', type=click.Choice(['internal', 'external', 'certification']), default='internal')
def schedule(audit_date, auditor, type):
    """Planifie un audit"""
    helper = AuditHelper()

    audit_info = {
        'date': audit_date,
        'auditor': auditor,
        'type': type,
        'scheduled_at': datetime.now().isoformat()
    }

    helper.schedule_audit(audit_info)
    console.print(f"[bold green]✓ Audit planifié pour le {audit_date}[/bold green]")

    if type == 'certification':
        console.print("\n[yellow]Préparation recommandée:[/yellow]")
        console.print("  1. Exécuter: iso27001 audit readiness")
        console.print("  2. Exécuter: iso27001 audit gap-analysis")
        console.print("  3. Exécuter: iso27001 audit prepare-evidence")
        console.print("  4. Exécuter: iso27001 controls report")
        console.print("  5. Exécuter: iso27001 risks report")


@audit.command()
@click.option('--output', '-o', default='output/soa.md', help='Fichier de sortie')
def generate_soa(output):
    """Génère la Déclaration d'Applicabilité (Statement of Applicability)"""
    console.print("[bold cyan]Génération de la Déclaration d'Applicabilité[/bold cyan]\n")

    helper = AuditHelper()
    engine = TemplateEngine()

    # Générer la SOA
    soa_data = helper.generate_soa()

    # Utiliser le template
    content = engine.render_soa(soa_data)

    # Sauvegarder
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding='utf-8')

    console.print(f"[bold green]✓ Déclaration d'Applicabilité générée[/bold green]")
    console.print(f"[dim]Emplacement: {output_path.absolute()}[/dim]")

    # Statistiques
    total = soa_data['total_controls']
    applicable = soa_data['applicable_controls']
    implemented = soa_data['implemented_controls']

    console.print(f"\n[yellow]Statistiques:[/yellow]")
    console.print(f"  • Contrôles applicables: {applicable}/{total}")
    console.print(f"  • Contrôles implémentés: {implemented}/{applicable}")
    console.print(f"  • Taux d'implémentation: {implemented/applicable*100:.1f}%")
