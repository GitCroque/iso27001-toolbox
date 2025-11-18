"""
Configuration du logging pour ISO 27001 Toolkit
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str = 'iso27001_toolkit',
    level: int = logging.INFO,
    log_file: Optional[Path] = None
) -> logging.Logger:
    """
    Configure et retourne un logger

    Args:
        name: Nom du logger
        level: Niveau de log
        log_file: Fichier de log optionnel

    Returns:
        Logger configuré
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Éviter les doublons
    if logger.handlers:
        return logger

    # Format des logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler pour la console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler pour fichier si spécifié
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str = 'iso27001_toolkit') -> logging.Logger:
    """
    Récupère un logger existant ou en crée un nouveau

    Args:
        name: Nom du logger

    Returns:
        Logger
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name)
    return logger
