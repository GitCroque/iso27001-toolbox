"""
Module de validation des entrées utilisateur
"""

import re
from datetime import datetime
from typing import Optional, List, Any
from pathlib import Path

from iso27001_toolkit.exceptions import ValidationError


def validate_email(email: str) -> str:
    """
    Valide une adresse email

    Args:
        email: Adresse email à valider

    Returns:
        L'email validé

    Raises:
        ValidationError: Si l'email est invalide
    """
    if not email:
        raise ValidationError("L'adresse email ne peut pas être vide")

    # Pattern regex pour valider l'email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError(f"Adresse email invalide: {email}")

    return email.strip()


def validate_date(date_str: str, date_format: str = "%Y-%m-%d") -> datetime:
    """
    Valide et parse une date

    Args:
        date_str: Date au format string
        date_format: Format de la date (défaut: YYYY-MM-DD)

    Returns:
        Objet datetime

    Raises:
        ValidationError: Si la date est invalide
    """
    if not date_str:
        raise ValidationError("La date ne peut pas être vide")

    try:
        return datetime.strptime(date_str, date_format)
    except ValueError as e:
        raise ValidationError(
            f"Format de date invalide: {date_str}. "
            f"Format attendu: {date_format}"
        ) from e


def validate_risk_score(score: Any, min_val: int = 1, max_val: int = 5) -> int:
    """
    Valide un score de risque

    Args:
        score: Score à valider
        min_val: Valeur minimale (défaut: 1)
        max_val: Valeur maximale (défaut: 5)

    Returns:
        Le score validé

    Raises:
        ValidationError: Si le score est invalide
    """
    try:
        score_int = int(score)
    except (TypeError, ValueError) as e:
        raise ValidationError(
            f"Le score doit être un nombre entier, reçu: {score}"
        ) from e

    if not min_val <= score_int <= max_val:
        raise ValidationError(
            f"Le score doit être entre {min_val} et {max_val}, reçu: {score_int}"
        )

    return score_int


def validate_choice(value: str, valid_choices: List[str]) -> str:
    """
    Valide qu'une valeur fait partie d'une liste de choix valides

    Args:
        value: Valeur à valider
        valid_choices: Liste des choix valides

    Returns:
        La valeur validée

    Raises:
        ValidationError: Si la valeur n'est pas dans les choix valides
    """
    if not value:
        raise ValidationError("La valeur ne peut pas être vide")

    if value not in valid_choices:
        raise ValidationError(
            f"Valeur invalide: {value}. "
            f"Choix valides: {', '.join(valid_choices)}"
        )

    return value


def validate_non_empty(value: str, field_name: str = "Champ") -> str:
    """
    Valide qu'une chaîne n'est pas vide

    Args:
        value: Valeur à valider
        field_name: Nom du champ pour le message d'erreur

    Returns:
        La valeur validée

    Raises:
        ValidationError: Si la valeur est vide
    """
    if not value or not value.strip():
        raise ValidationError(f"{field_name} ne peut pas être vide")

    return value.strip()


def validate_integer_range(
    value: Any,
    min_val: Optional[int] = None,
    max_val: Optional[int] = None,
    field_name: str = "Valeur"
) -> int:
    """
    Valide qu'un entier est dans une plage donnée

    Args:
        value: Valeur à valider
        min_val: Valeur minimale (optionnel)
        max_val: Valeur maximale (optionnel)
        field_name: Nom du champ pour le message d'erreur

    Returns:
        La valeur validée

    Raises:
        ValidationError: Si la valeur est invalide
    """
    try:
        int_val = int(value)
    except (TypeError, ValueError) as e:
        raise ValidationError(
            f"{field_name} doit être un nombre entier, reçu: {value}"
        ) from e

    if min_val is not None and int_val < min_val:
        raise ValidationError(
            f"{field_name} doit être supérieur ou égal à {min_val}, reçu: {int_val}"
        )

    if max_val is not None and int_val > max_val:
        raise ValidationError(
            f"{field_name} doit être inférieur ou égal à {max_val}, reçu: {int_val}"
        )

    return int_val


def validate_url(url: str) -> str:
    """
    Valide une URL

    Args:
        url: URL à valider

    Returns:
        L'URL validée

    Raises:
        ValidationError: Si l'URL est invalide
    """
    if not url:
        raise ValidationError("L'URL ne peut pas être vide")

    # Pattern regex basique pour URL
    pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'
    if not re.match(pattern, url):
        raise ValidationError(f"URL invalide: {url}")

    return url.strip()


def validate_file_path(
    file_path: str,
    must_exist: bool = False,
    must_be_file: bool = True
) -> Path:
    """
    Valide un chemin de fichier

    Args:
        file_path: Chemin à valider
        must_exist: Le fichier doit exister (défaut: False)
        must_be_file: Doit être un fichier (pas un dossier) (défaut: True)

    Returns:
        Objet Path validé

    Raises:
        ValidationError: Si le chemin est invalide
    """
    if not file_path:
        raise ValidationError("Le chemin de fichier ne peut pas être vide")

    path = Path(file_path)

    if must_exist and not path.exists():
        raise ValidationError(f"Le chemin n'existe pas: {file_path}")

    if must_exist and must_be_file and not path.is_file():
        raise ValidationError(f"Le chemin n'est pas un fichier: {file_path}")

    return path


def validate_control_id(control_id: str) -> str:
    """
    Valide un ID de contrôle ISO 27001 (format: A.X.Y)

    Args:
        control_id: ID du contrôle

    Returns:
        L'ID validé

    Raises:
        ValidationError: Si l'ID est invalide
    """
    if not control_id:
        raise ValidationError("L'ID du contrôle ne peut pas être vide")

    # Format: A.X.Y où X est 5-8 et Y est 1-99
    pattern = r'^A\.[5-8]\.\d{1,2}$'
    if not re.match(pattern, control_id):
        raise ValidationError(
            f"Format d'ID de contrôle invalide: {control_id}. "
            f"Format attendu: A.X.Y (ex: A.5.1, A.8.23)"
        )

    return control_id


def validate_percentage(value: Any) -> float:
    """
    Valide un pourcentage (0-100)

    Args:
        value: Valeur à valider

    Returns:
        Le pourcentage validé

    Raises:
        ValidationError: Si la valeur est invalide
    """
    try:
        percent = float(value)
    except (TypeError, ValueError) as e:
        raise ValidationError(
            f"Le pourcentage doit être un nombre, reçu: {value}"
        ) from e

    if not 0 <= percent <= 100:
        raise ValidationError(
            f"Le pourcentage doit être entre 0 et 100, reçu: {percent}"
        )

    return percent


def sanitize_filename(filename: str) -> str:
    """
    Nettoie un nom de fichier en retirant les caractères dangereux

    Args:
        filename: Nom de fichier à nettoyer

    Returns:
        Nom de fichier nettoyé

    Raises:
        ValidationError: Si le nom de fichier est invalide
    """
    if not filename:
        raise ValidationError("Le nom de fichier ne peut pas être vide")

    # Retirer les caractères dangereux
    sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', filename)

    # Retirer les espaces en début/fin
    sanitized = sanitized.strip()

    # Vérifier que le nom n'est pas vide après nettoyage
    if not sanitized:
        raise ValidationError("Le nom de fichier contient uniquement des caractères invalides")

    return sanitized
