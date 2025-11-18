"""
Commandes pour l'export PDF des documents ISO 27001
"""

import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from datetime import datetime

from iso27001_toolkit.utils.pdf_exporter import get_pdf_exporter, check_pdf_support
from iso27001_toolkit.utils import config
from iso27001_toolkit.logger import get_logger

console = Console()
logger = get_logger(__name__)


@click.group()
def export():
    """Export de documents au format PDF"""
    if not check_pdf_support():
        console.print(
            Panel(
                "[bold red]❌ Export PDF non disponible[/bold red]\n\n"
                "Les dépendances WeasyPrint et markdown2 sont requises.\n\n"
                "Installez-les avec:\n"
                "[cyan]pip install weasyprint markdown2[/cyan]",
                title="Erreur",
                border_style="red"
            )
        )
        raise click.Abort()


@export.command()
@click.argument('markdown_file', type=click.Path(exists=True, path_type=Path))
@click.option('--output', '-o', type=click.Path(path_type=Path), help='Fichier PDF de sortie')
@click.option('--title', '-t', help='Titre du document (déduit automatiquement si non fourni)')
@click.option('--type', '-T', 'doc_type',
              type=click.Choice(['policy', 'soa', 'risks', 'audit', 'generic']),
              default='generic',
              help='Type de document (détermine le style)')
@click.option('--organization', '-org', help='Nom de l\'organisation (lu depuis la config si non fourni)')
@click.option('--no-cover', is_flag=True, help='Ne pas générer de page de couverture')
def pdf(markdown_file, output, title, doc_type, organization, no_cover):
    """
    Convertit un fichier Markdown en PDF professionnel

    Exemples:
        iso27001 export pdf policy.md -o policy.pdf --type policy
        iso27001 export pdf soa.md --type soa
        iso27001 export pdf custom.md -t "Mon Rapport" --no-cover
    """
    console.print(f"[bold cyan]📄 Export PDF: {markdown_file.name}[/bold cyan]\n")

    # Déterminer le fichier de sortie
    if output is None:
        output = markdown_file.with_suffix('.pdf')

    # Lire l'organisation depuis la config si non fournie
    if organization is None:
        try:
            org_file = config.CONFIG_DIR / "organization.yml"
            if org_file.exists():
                import yaml
                with open(org_file, 'r', encoding='utf-8') as f:
                    org_data = yaml.safe_load(f)
                    organization = org_data.get('name', 'Organisation')
            else:
                organization = "Organisation"
        except Exception as e:
            logger.warning(f"Impossible de lire l'organisation: {e}")
            organization = "Organisation"

    try:
        exporter = get_pdf_exporter()

        # Exporter selon le type
        if doc_type == 'policy':
            result = exporter.export_policy_pdf(
                policy_file=markdown_file,
                output_pdf=output,
                organization=organization
            )
        elif doc_type == 'soa':
            result = exporter.export_soa_pdf(
                soa_file=markdown_file,
                output_pdf=output,
                organization=organization
            )
        elif doc_type == 'risks':
            result = exporter.export_risk_register_pdf(
                risk_file=markdown_file,
                output_pdf=output,
                organization=organization
            )
        elif doc_type == 'audit':
            result = exporter.export_audit_report_pdf(
                audit_file=markdown_file,
                output_pdf=output,
                organization=organization
            )
        else:  # generic
            result = exporter.markdown_to_pdf(
                markdown_file=markdown_file,
                output_pdf=output,
                title=title,
                organization=organization,
                add_cover=not no_cover
            )

        console.print(f"[bold green]✓ PDF généré avec succès![/bold green]")
        console.print(f"[dim]Emplacement: {result.absolute()}[/dim]")
        console.print(f"[dim]Taille: {result.stat().st_size / 1024:.1f} KB[/dim]")

    except ImportError as e:
        console.print(f"[bold red]❌ Erreur: {e}[/bold red]")
        raise click.Abort()
    except Exception as e:
        console.print(f"[bold red]❌ Erreur lors de l'export PDF: {e}[/bold red]")
        logger.error(f"Erreur export PDF: {e}", exc_info=True)
        raise click.Abort()


@export.command()
@click.option('--output-dir', '-o', type=click.Path(path_type=Path), default='output/pdf',
              help='Répertoire de sortie pour les PDFs')
@click.option('--organization', '-org', help='Nom de l\'organisation')
def policies(output_dir, organization):
    """
    Exporte toutes les politiques disponibles en PDF

    Recherche les fichiers .md de politiques et les convertit en PDF.
    """
    console.print("[bold cyan]📚 Export de toutes les politiques en PDF[/bold cyan]\n")

    # Trouver les politiques
    policy_dir = Path('output/policies')
    if not policy_dir.exists():
        console.print(f"[yellow]⚠️  Aucune politique trouvée dans {policy_dir}[/yellow]")
        console.print("[dim]Générez d'abord les politiques avec: iso27001 policies generate[/dim]")
        return

    policy_files = list(policy_dir.glob('*.md'))
    if not policy_files:
        console.print(f"[yellow]⚠️  Aucun fichier .md trouvé dans {policy_dir}[/yellow]")
        return

    # Lire l'organisation
    if organization is None:
        try:
            org_file = config.CONFIG_DIR / "organization.yml"
            if org_file.exists():
                import yaml
                with open(org_file, 'r', encoding='utf-8') as f:
                    org_data = yaml.safe_load(f)
                    organization = org_data.get('name', 'Organisation')
            else:
                organization = "Organisation"
        except:
            organization = "Organisation"

    # Créer le répertoire de sortie
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Exporter chaque politique
    exporter = get_pdf_exporter()
    success_count = 0
    error_count = 0

    with console.status("[bold green]Export en cours...") as status:
        for policy_file in policy_files:
            try:
                status.update(f"[bold green]Export de {policy_file.name}...")
                output_pdf = output_dir / policy_file.with_suffix('.pdf').name

                exporter.export_policy_pdf(
                    policy_file=policy_file,
                    output_pdf=output_pdf,
                    organization=organization
                )

                console.print(f"[green]✓[/green] {policy_file.name} → {output_pdf.name}")
                success_count += 1

            except Exception as e:
                console.print(f"[red]✗[/red] {policy_file.name}: {e}")
                logger.error(f"Erreur export {policy_file}: {e}")
                error_count += 1

    # Résumé
    console.print(f"\n[bold]Résumé:[/bold]")
    console.print(f"  [green]✓ {success_count} PDFs générés avec succès[/green]")
    if error_count > 0:
        console.print(f"  [red]✗ {error_count} erreurs[/red]")
    console.print(f"  [dim]Répertoire: {output_dir.absolute()}[/dim]")


@export.command()
@click.option('--output', '-o', type=click.Path(path_type=Path),
              default='output/pdf/soa.pdf',
              help='Fichier PDF de sortie')
@click.option('--organization', '-org', help='Nom de l\'organisation')
def soa(output, organization):
    """
    Exporte le Statement of Applicability (SoA) en PDF

    Génère d'abord le SoA en markdown puis le convertit en PDF.
    """
    console.print("[bold cyan]📋 Export du Statement of Applicability (SoA)[/bold cyan]\n")

    # Lire l'organisation
    if organization is None:
        try:
            org_file = config.CONFIG_DIR / "organization.yml"
            if org_file.exists():
                import yaml
                with open(org_file, 'r', encoding='utf-8') as f:
                    org_data = yaml.safe_load(f)
                    organization = org_data.get('name', 'Organisation')
            else:
                organization = "Organisation"
        except:
            organization = "Organisation"

    # Générer le SoA en markdown d'abord
    console.print("[dim]Génération du SoA en markdown...[/dim]")
    from iso27001_toolkit.utils.audit_helper import AuditHelper

    helper = AuditHelper()
    soa_data = helper.generate_soa()

    # Sauvegarder le markdown temporaire
    temp_md = Path('output/soa_temp.md')
    temp_md.parent.mkdir(parents=True, exist_ok=True)

    with open(temp_md, 'w', encoding='utf-8') as f:
        f.write(f"# Statement of Applicability (SoA)\n\n")
        f.write(f"**Organisation:** {organization}\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%d/%m/%Y')}\n\n")
        f.write(f"**Norme:** ISO/IEC 27001:2022\n\n")
        f.write("---\n\n")
        f.write(soa_data)

    # Convertir en PDF
    try:
        exporter = get_pdf_exporter()

        # Calculer le score de maturité
        from iso27001_toolkit.utils.controls_tracker import ControlsTracker
        tracker = ControlsTracker()
        stats = tracker.get_statistics()
        total = stats['total']
        implemented = stats['by_status'].get('implemented', 0) + stats['by_status'].get('verified', 0)
        maturity_score = (implemented / total * 100) if total > 0 else 0

        output_path = Path(output)
        result = exporter.export_soa_pdf(
            soa_file=temp_md,
            output_pdf=output_path,
            organization=organization,
            maturity_score=maturity_score
        )

        # Nettoyer le fichier temporaire
        temp_md.unlink()

        console.print(f"[bold green]✓ SoA PDF généré avec succès![/bold green]")
        console.print(f"[dim]Emplacement: {result.absolute()}[/dim]")
        console.print(f"[dim]Contrôles: {implemented}/{total} implémentés ({maturity_score:.1f}%)[/dim]")

    except Exception as e:
        console.print(f"[bold red]❌ Erreur: {e}[/bold red]")
        logger.error(f"Erreur export SoA: {e}", exc_info=True)
        if temp_md.exists():
            temp_md.unlink()
        raise click.Abort()


@export.command()
@click.option('--output', '-o', type=click.Path(path_type=Path),
              default='output/pdf/risk_register.pdf',
              help='Fichier PDF de sortie')
@click.option('--organization', '-org', help='Nom de l\'organisation')
def risks(output, organization):
    """
    Exporte le registre des risques en PDF

    Génère d'abord le registre en markdown puis le convertit en PDF.
    """
    console.print("[bold cyan]⚠️  Export du registre des risques[/bold cyan]\n")

    # Lire l'organisation
    if organization is None:
        try:
            org_file = config.CONFIG_DIR / "organization.yml"
            if org_file.exists():
                import yaml
                with open(org_file, 'r', encoding='utf-8') as f:
                    org_data = yaml.safe_load(f)
                    organization = org_data.get('name', 'Organisation')
            else:
                organization = "Organisation"
        except:
            organization = "Organisation"

    # Générer le registre en markdown
    console.print("[dim]Génération du registre des risques en markdown...[/dim]")
    from iso27001_toolkit.utils.audit_helper import AuditHelper

    helper = AuditHelper()
    risk_data = helper.generate_risk_register()

    # Compter les risques
    from iso27001_toolkit.utils.risk_manager import RiskManager
    risk_mgr = RiskManager()
    all_risks = risk_mgr.list_risks()
    total_risks = len(all_risks)

    # Sauvegarder le markdown temporaire
    temp_md = Path('output/risk_register_temp.md')
    temp_md.parent.mkdir(parents=True, exist_ok=True)

    with open(temp_md, 'w', encoding='utf-8') as f:
        f.write(f"# Registre des Risques ISO 27001\n\n")
        f.write(f"**Organisation:** {organization}\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%d/%m/%Y')}\n\n")
        f.write(f"**Risques identifiés:** {total_risks}\n\n")
        f.write("---\n\n")
        f.write(risk_data)

    # Convertir en PDF
    try:
        exporter = get_pdf_exporter()

        output_path = Path(output)
        result = exporter.export_risk_register_pdf(
            risk_file=temp_md,
            output_pdf=output_path,
            organization=organization,
            total_risks=total_risks
        )

        # Nettoyer
        temp_md.unlink()

        console.print(f"[bold green]✓ Registre des risques PDF généré avec succès![/bold green]")
        console.print(f"[dim]Emplacement: {result.absolute()}[/dim]")
        console.print(f"[dim]Risques: {total_risks} identifiés[/dim]")

    except Exception as e:
        console.print(f"[bold red]❌ Erreur: {e}[/bold red]")
        logger.error(f"Erreur export risques: {e}", exc_info=True)
        if temp_md.exists():
            temp_md.unlink()
        raise click.Abort()


@export.command()
@click.option('--output-dir', '-o', type=click.Path(path_type=Path),
              default='output/pdf',
              help='Répertoire de sortie pour les PDFs')
@click.option('--organization', '-org', help='Nom de l\'organisation')
def all(output_dir, organization):
    """
    Exporte tous les documents (SoA, risques, politiques) en PDF

    Génère un package complet de documentation PDF.
    """
    console.print("[bold cyan]📦 Export complet de tous les documents en PDF[/bold cyan]\n")

    # Lire l'organisation
    if organization is None:
        try:
            org_file = config.CONFIG_DIR / "organization.yml"
            if org_file.exists():
                import yaml
                with open(org_file, 'r', encoding='utf-8') as f:
                    org_data = yaml.safe_load(f)
                    organization = org_data.get('name', 'Organisation')
            else:
                organization = "Organisation"
        except:
            organization = "Organisation"

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    total_success = 0
    total_errors = 0

    # 1. Export SoA
    console.print("\n[bold]1. Export du SoA...[/bold]")
    try:
        ctx = click.get_current_context()
        ctx.invoke(soa, output=output_dir / 'soa.pdf', organization=organization)
        total_success += 1
    except:
        total_errors += 1

    # 2. Export Risques
    console.print("\n[bold]2. Export du registre des risques...[/bold]")
    try:
        ctx = click.get_current_context()
        ctx.invoke(risks, output=output_dir / 'risk_register.pdf', organization=organization)
        total_success += 1
    except:
        total_errors += 1

    # 3. Export Politiques
    console.print("\n[bold]3. Export des politiques...[/bold]")
    policies_dir = output_dir / 'policies'
    policies_dir.mkdir(exist_ok=True)
    try:
        ctx = click.get_current_context()
        ctx.invoke(policies, output_dir=policies_dir, organization=organization)
        # Compter comme 1 succès (déjà compté dans la commande policies)
    except:
        total_errors += 1

    # Résumé final
    console.print(Panel(
        f"[bold]Export complet terminé![/bold]\n\n"
        f"[green]✓ Succès: {total_success}[/green]\n"
        f"[red]✗ Erreurs: {total_errors}[/red]\n\n"
        f"[dim]Répertoire: {output_dir.absolute()}[/dim]",
        title="[cyan]Résumé[/cyan]",
        border_style="cyan"
    ))
