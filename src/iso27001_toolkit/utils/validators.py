"""
Validators pour les entrées utilisateur
"""

import re
from typing import Any, List, Optional
from datetime import datetime


class ValidationError(Exception):
    """Exception levée lors d'une erreur de validation"""
    pass


def validate_email(email: str) -> bool:
    """
    Valide un email

    Args:
        email: Adresse email à valider

    Returns:
        True si valide

    Raises:
        ValidationError: Si l'email est invalide
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError(f"Email invalide: {email}")
    return True


def validate_date(date_str: str, format: str = '%Y-%m-%d') -> bool:
    """
    Valide une date

    Args:
        date_str: Date sous forme de chaîne
        format: Format attendu

    Returns:
        True si valide

    Raises:
        ValidationError: Si la date est invalide
    """
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        raise ValidationError(f"Date invalide: {date_str} (format attendu: {format})")


def validate_control_id(control_id: str) -> bool:
    """
    Valide un ID de contrôle ISO 27001

    Args:
        control_id: ID du contrôle (ex: A.5.1)

    Returns:
        True si valide

    Raises:
        ValidationError: Si l'ID est invalide
    """
    pattern = r'^A\.[5-8]\.\d+$'
    if not re.match(pattern, control_id.upper()):
        raise ValidationError(
            f"ID de contrôle invalide: {control_id}. "
            "Format attendu: A.X.Y (ex: A.5.1)"
        )
    return True


def validate_control_status(status: str) -> bool:
    """
    Valide un statut de contrôle

    Args:
        status: Statut du contrôle

    Returns:
        True si valide

    Raises:
        ValidationError: Si le statut est invalide
    """
    valid_statuses = ['not_started', 'in_progress', 'implemented', 'verified']
    if status not in valid_statuses:
        raise ValidationError(
            f"Statut invalide: {status}. "
            f"Valeurs valides: {', '.join(valid_statuses)}"
        )
    return True


def validate_priority(priority: str) -> bool:
    """
    Valide une priorité

    Args:
        priority: Priorité

    Returns:
        True si valide

    Raises:
        ValidationError: Si la priorité est invalide
    """
    valid_priorities = ['low', 'medium', 'high']
    if priority not in valid_priorities:
        raise ValidationError(
            f"Priorité invalide: {priority}. "
            f"Valeurs valides: {', '.join(valid_priorities)}"
        )
    return True


def validate_risk_level(level: str) -> bool:
    """
    Valide un niveau de risque

    Args:
        level: Niveau de risque

    Returns:
        True si valide

    Raises:
        ValidationError: Si le niveau est invalide
    """
    valid_levels = ['low', 'medium', 'high', 'critical']
    if level not in valid_levels:
        raise ValidationError(
            f"Niveau de risque invalide: {level}. "
            f"Valeurs valides: {', '.join(valid_levels)}"
        )
    return True


def validate_risk_category(category: str) -> bool:
    """
    Valide une catégorie de risque

    Args:
        category: Catégorie du risque

    Returns:
        True si valide

    Raises:
        ValidationError: Si la catégorie est invalide
    """
    valid_categories = [
        'confidentiality', 'integrity', 'availability',
        'compliance', 'operational', 'strategic', 'financial'
    ]
    if category not in valid_categories:
        raise ValidationError(
            f"Catégorie invalide: {category}. "
            f"Valeurs valides: {', '.join(valid_categories)}"
        )
    return True


def validate_risk_treatment(treatment: str) -> bool:
    """
    Valide un type de traitement de risque

    Args:
        treatment: Type de traitement

    Returns:
        True si valide

    Raises:
        ValidationError: Si le traitement est invalide
    """
    valid_treatments = ['mitigate', 'accept', 'transfer', 'avoid']
    if treatment not in valid_treatments:
        raise ValidationError(
            f"Traitement invalide: {treatment}. "
            f"Valeurs valides: {', '.join(valid_treatments)}"
        )
    return True


def validate_impact_likelihood(value: int) -> bool:
    """
    Valide une valeur d'impact ou de probabilité (1-5)

    Args:
        value: Valeur à valider

    Returns:
        True si valide

    Raises:
        ValidationError: Si la valeur est invalide
    """
    if not isinstance(value, int):
        raise ValidationError(f"Valeur doit être un entier: {value}")

    if not 1 <= value <= 5:
        raise ValidationError(
            f"Valeur invalide: {value}. "
            "Doit être entre 1 et 5"
        )
    return True


def validate_required(value: Any, field_name: str) -> bool:
    """
    Valide qu'un champ requis est présent

    Args:
        value: Valeur à vérifier
        field_name: Nom du champ

    Returns:
        True si présent

    Raises:
        ValidationError: Si le champ est vide
    """
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ValidationError(f"Le champ '{field_name}' est requis")
    return True


def validate_file_path(path: str, must_exist: bool = False) -> bool:
    """
    Valide un chemin de fichier

    Args:
        path: Chemin du fichier
        must_exist: Si True, vérifie que le fichier existe

    Returns:
        True si valide

    Raises:
        ValidationError: Si le chemin est invalide
    """
    from pathlib import Path

    if not path:
        raise ValidationError("Chemin de fichier vide")

    path_obj = Path(path)

    if must_exist and not path_obj.exists():
        raise ValidationError(f"Le fichier n'existe pas: {path}")

    # Vérifier les caractères interdits
    invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
    if any(char in path for char in invalid_chars):
        raise ValidationError(f"Chemin contient des caractères invalides: {path}")

    return True


def validate_organization_config(config: dict) -> bool:
    """
    Valide une configuration d'organisation

    Args:
        config: Configuration à valider

    Returns:
        True si valide

    Raises:
        ValidationError: Si la configuration est invalide
    """
    required_fields = [
        'organization_name',
        'ciso_name',
        'ciso_email',
        'effective_date'
    ]

    for field in required_fields:
        validate_required(config.get(field), field)

    # Valider l'email du RSSI
    if 'ciso_email' in config:
        validate_email(config['ciso_email'])

    # Valider l'email du DPO si présent
    if config.get('dpo_email'):
        validate_email(config['dpo_email'])

    # Valider la date d'effet
    if 'effective_date' in config:
        validate_date(config['effective_date'])

    # Valider la période de révision
    if 'review_period' in config:
        period = config['review_period']
        if isinstance(period, str):
            period = int(period)
        if not 1 <= period <= 36:
            raise ValidationError(
                "La période de révision doit être entre 1 et 36 mois"
            )

    return True
