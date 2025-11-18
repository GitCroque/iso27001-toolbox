"""
Commandes pour la génération de politiques de sécurité
"""

import click
import os
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm

from iso27001_toolkit.utils.template_engine import TemplateEngine
from iso27001_toolkit.utils.config import load_organization_config, save_organization_config

console = Console()


@click.group()
def policies():
    """Génération et gestion des politiques de sécurité ISO 27001"""
    pass


@policies.command()
@click.option('--output', '-o', default='output/policies', help='Répertoire de sortie')
@click.option('--policy', '-p', help='Nom de la politique spécifique à générer')
@click.option('--interactive', '-i', is_flag=True, help='Mode interactif pour configurer les variables')
def generate(output, policy, interactive):
    """Génère les politiques de sécurité à partir des templates"""
    console.print("[bold cyan]Génération des politiques de sécurité ISO 27001[/bold cyan]\n")

    # Charger ou créer la configuration de l'organisation
    config = load_organization_config()

    if interactive or not config:
        console.print("[yellow]Configuration de votre organisation:[/yellow]\n")
        config = {
            'organization_name': Prompt.ask("Nom de l'organisation", default=config.get('organization_name', 'Mon Entreprise')),
            'organization_address': Prompt.ask("Adresse", default=config.get('organization_address', '')),
            'organization_city': Prompt.ask("Ville", default=config.get('organization_city', '')),
            'organization_country': Prompt.ask("Pays", default=config.get('organization_country', 'France')),
            'ciso_name': Prompt.ask("Nom du RSSI", default=config.get('ciso_name', '')),
            'ciso_email': Prompt.ask("Email du RSSI", default=config.get('ciso_email', '')),
            'dpo_name': Prompt.ask("Nom du DPO", default=config.get('dpo_name', '')),
            'dpo_email': Prompt.ask("Email du DPO", default=config.get('dpo_email', '')),
            'effective_date': Prompt.ask("Date d'effet", default=config.get('effective_date', '2024-01-01')),
            'review_period': Prompt.ask("Période de révision (mois)", default=str(config.get('review_period', 12))),
        }

        if Confirm.ask("Sauvegarder cette configuration ?"):
            save_organization_config(config)
            console.print("[green]✓[/green] Configuration sauvegardée\n")

    # Initialiser le moteur de templates
    engine = TemplateEngine()

    # Créer le répertoire de sortie
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)

    # Liste des politiques disponibles
    available_policies = [
        'information_security_policy',
        'access_control_policy',
        'asset_management_policy',
        'cryptography_policy',
        'physical_security_policy',
        'operations_security_policy',
        'communications_security_policy',
        'supplier_relationships_policy',
        'incident_management_policy',
        'business_continuity_policy',
        'compliance_policy',
    ]

    if policy:
        policies_to_generate = [policy] if policy in available_policies else []
        if not policies_to_generate:
            console.print(f"[red]✗[/red] Politique '{policy}' non trouvée")
            return
    else:
        policies_to_generate = available_policies

    # Générer les politiques
    generated = []
    for policy_name in policies_to_generate:
        try:
            content = engine.render_policy(policy_name, config)
            output_file = output_path / f"{policy_name}.md"
            output_file.write_text(content, encoding='utf-8')
            generated.append(policy_name)
            console.print(f"[green]✓[/green] {policy_name}.md généré")
        except Exception as e:
            console.print(f"[red]✗[/red] Erreur lors de la génération de {policy_name}: {e}")

    console.print(f"\n[bold green]✓ {len(generated)} politique(s) générée(s)[/bold green]")
    console.print(f"[dim]Emplacement: {output_path.absolute()}[/dim]")


@policies.command()
def list():
    """Liste toutes les politiques disponibles"""
    console.print("[bold cyan]Politiques ISO 27001 disponibles[/bold cyan]\n")

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Politique", style="cyan")
    table.add_column("Description")
    table.add_column("Annexe A", style="yellow")

    policies_info = [
        ("information_security_policy", "Politique générale de sécurité de l'information", "A.5.1"),
        ("access_control_policy", "Politique de contrôle d'accès", "A.5.15-18"),
        ("asset_management_policy", "Politique de gestion des actifs", "A.5.9-14"),
        ("cryptography_policy", "Politique de cryptographie", "A.8.24"),
        ("physical_security_policy", "Politique de sécurité physique", "A.7.1-14"),
        ("operations_security_policy", "Politique de sécurité des opérations", "A.8.1-34"),
        ("communications_security_policy", "Politique de sécurité des communications", "A.5.13-14"),
        ("supplier_relationships_policy", "Politique de gestion des fournisseurs", "A.5.19-23"),
        ("incident_management_policy", "Politique de gestion des incidents", "A.5.24-28"),
        ("business_continuity_policy", "Politique de continuité d'activité", "A.5.29-30"),
        ("compliance_policy", "Politique de conformité", "A.5.31-37"),
    ]

    for policy, desc, annex in policies_info:
        table.add_row(policy, desc, annex)

    console.print(table)


@policies.command()
def configure():
    """Configure les informations de l'organisation"""
    console.print("[bold cyan]Configuration de l'organisation[/bold cyan]\n")

    config = load_organization_config()

    config = {
        'organization_name': Prompt.ask("Nom de l'organisation", default=config.get('organization_name', 'Mon Entreprise')),
        'organization_address': Prompt.ask("Adresse", default=config.get('organization_address', '')),
        'organization_city': Prompt.ask("Ville", default=config.get('organization_city', '')),
        'organization_country': Prompt.ask("Pays", default=config.get('organization_country', 'France')),
        'ciso_name': Prompt.ask("Nom du RSSI", default=config.get('ciso_name', '')),
        'ciso_email': Prompt.ask("Email du RSSI", default=config.get('ciso_email', '')),
        'dpo_name': Prompt.ask("Nom du DPO", default=config.get('dpo_name', '')),
        'dpo_email': Prompt.ask("Email du DPO", default=config.get('dpo_email', '')),
        'effective_date': Prompt.ask("Date d'effet", default=config.get('effective_date', '2024-01-01')),
        'review_period': Prompt.ask("Période de révision (mois)", default=str(config.get('review_period', 12))),
    }

    save_organization_config(config)
    console.print("\n[bold green]✓ Configuration sauvegardée avec succès[/bold green]")
