"""
Configuration du système de logging pour ISO 27001 Toolkit
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional


def setup_logger(
    name: str = "iso27001_toolkit",
    log_level: str = "INFO",
    log_dir: Optional[Path] = None
) -> logging.Logger:
    """
    Configure et retourne un logger pour l'application

    Args:
        name: Nom du logger
        log_level: Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Répertoire des logs (défaut: ~/.iso27001/logs)

    Returns:
        Logger configuré
    """
    logger = logging.getLogger(name)

    # Éviter de reconfigurer si déjà fait
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, log_level.upper()))

    # Format des logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler pour la console (seulement WARNING et au-dessus)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler pour le fichier de log
    if log_dir is None:
        log_dir = Path.home() / ".iso27001" / "logs"

    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "iso27001_toolkit.log"

    # Rotation des logs : 5 fichiers de 5 MB max
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "iso27001_toolkit") -> logging.Logger:
    """
    Récupère ou crée un logger

    Args:
        name: Nom du logger

    Returns:
        Logger
    """
    logger = logging.getLogger(name)

    # Si le logger n'a pas de handlers, le configurer
    if not logger.handlers:
        return setup_logger(name)

    return logger


# Logger global pour l'application
logger = get_logger()
