"""
Gestion de la configuration de l'organisation
"""

import yaml
from pathlib import Path
from typing import Dict, Any


CONFIG_DIR = Path.home() / '.iso27001'
CONFIG_FILE = CONFIG_DIR / 'config.yml'


def ensure_config_dir():
    """Crée le répertoire de configuration s'il n'existe pas"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_organization_config() -> Dict[str, Any]:
    """Charge la configuration de l'organisation"""
    ensure_config_dir()

    if not CONFIG_FILE.exists():
        return {}

    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def save_organization_config(config: Dict[str, Any]):
    """Sauvegarde la configuration de l'organisation"""
    ensure_config_dir()

    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)


def get_data_dir() -> Path:
    """Retourne le répertoire de données"""
    data_dir = CONFIG_DIR / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_controls_file() -> Path:
    """Retourne le fichier de suivi des contrôles"""
    return get_data_dir() / 'controls.yml'


def get_risks_file() -> Path:
    """Retourne le fichier de gestion des risques"""
    return get_data_dir() / 'risks.yml'


def get_audit_file() -> Path:
    """Retourne le fichier de données d'audit"""
    return get_data_dir() / 'audit.yml'


def get_policies_dir() -> Path:
    """Retourne le répertoire des politiques générées"""
    policies_dir = CONFIG_DIR / 'policies'
    policies_dir.mkdir(parents=True, exist_ok=True)
    return policies_dir
