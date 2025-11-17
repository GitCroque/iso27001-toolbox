"""
Classe de base pour la gestion du stockage YAML
"""

import yaml
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

from iso27001_toolkit.exceptions import DataPersistenceError
from iso27001_toolkit.logger import get_logger


logger = get_logger(__name__)


class YAMLStorage:
    """
    Classe de base pour gérer le stockage et le chargement de données YAML

    Les classes enfants doivent définir:
    - self.file_path: Path - Le chemin du fichier YAML
    - self._get_default_data(): Dict - Les données par défaut
    """

    def __init__(self, file_path: Path, encrypt: bool = False):
        """
        Initialise le gestionnaire de stockage

        Args:
            file_path: Chemin du fichier YAML
            encrypt: Si True, chiffre les données (nécessite encryption_manager)
        """
        self.file_path = file_path
        self.encrypt = encrypt
        self.data: Dict[str, Any] = {}
        self.encryption_manager = None

        if encrypt:
            try:
                from iso27001_toolkit.utils.encryption import EncryptionManager
                self.encryption_manager = EncryptionManager()
            except ImportError:
                logger.warning("Module de chiffrement non disponible, données non chiffrées")
                self.encrypt = False

    def _get_default_data(self) -> Dict[str, Any]:
        """
        Retourne les données par défaut

        À surcharger dans les classes enfants

        Returns:
            Dictionnaire avec les données par défaut
        """
        return {'last_updated': None}

    def load(self) -> Dict[str, Any]:
        """
        Charge les données depuis le fichier YAML

        Returns:
            Dictionnaire avec les données

        Raises:
            DataPersistenceError: Si le chargement échoue
        """
        if not self.file_path.exists():
            logger.info(f"Fichier {self.file_path} n'existe pas, utilisation des données par défaut")
            self.data = self._get_default_data()
            return self.data

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()

                # Déchiffrer si nécessaire
                if self.encrypt and self.encryption_manager:
                    content = self.encryption_manager.decrypt(content)

                data = yaml.safe_load(content)
                self.data = data if data else self._get_default_data()

                logger.debug(f"Données chargées depuis {self.file_path}")
                return self.data

        except yaml.YAMLError as e:
            logger.error(f"Erreur lors du parsing YAML de {self.file_path}: {e}")
            raise DataPersistenceError(
                f"Impossible de lire le fichier {self.file_path}: {e}"
            ) from e
        except Exception as e:
            logger.error(f"Erreur lors du chargement de {self.file_path}: {e}")
            raise DataPersistenceError(
                f"Erreur lors du chargement des données: {e}"
            ) from e

    def save(self) -> None:
        """
        Sauvegarde les données dans le fichier YAML

        Raises:
            DataPersistenceError: Si la sauvegarde échoue
        """
        # Mettre à jour la date de dernière modification
        self.data['last_updated'] = datetime.now().isoformat()

        try:
            # Créer le répertoire parent si nécessaire
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            # Convertir en YAML
            content = yaml.dump(
                self.data,
                allow_unicode=True,
                default_flow_style=False,
                sort_keys=False
            )

            # Chiffrer si nécessaire
            if self.encrypt and self.encryption_manager:
                content = self.encryption_manager.encrypt(content)

            # Écrire dans le fichier
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.debug(f"Données sauvegardées dans {self.file_path}")

        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde dans {self.file_path}: {e}")
            raise DataPersistenceError(
                f"Impossible de sauvegarder les données: {e}"
            ) from e

    def backup(self, backup_path: Path = None) -> Path:
        """
        Crée une sauvegarde du fichier de données

        Args:
            backup_path: Chemin de la sauvegarde (optionnel)

        Returns:
            Chemin du fichier de sauvegarde

        Raises:
            DataPersistenceError: Si la sauvegarde échoue
        """
        if not self.file_path.exists():
            raise DataPersistenceError(f"Fichier {self.file_path} n'existe pas")

        if backup_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = self.file_path.parent / f"{self.file_path.stem}_backup_{timestamp}.yml"

        try:
            import shutil
            shutil.copy2(self.file_path, backup_path)
            logger.info(f"Sauvegarde créée: {backup_path}")
            return backup_path

        except Exception as e:
            logger.error(f"Erreur lors de la création de la sauvegarde: {e}")
            raise DataPersistenceError(
                f"Impossible de créer la sauvegarde: {e}"
            ) from e

    def restore(self, backup_path: Path) -> None:
        """
        Restaure les données depuis une sauvegarde

        Args:
            backup_path: Chemin de la sauvegarde

        Raises:
            DataPersistenceError: Si la restauration échoue
        """
        if not backup_path.exists():
            raise DataPersistenceError(f"Sauvegarde {backup_path} n'existe pas")

        try:
            import shutil
            shutil.copy2(backup_path, self.file_path)
            self.load()
            logger.info(f"Données restaurées depuis {backup_path}")

        except Exception as e:
            logger.error(f"Erreur lors de la restauration: {e}")
            raise DataPersistenceError(
                f"Impossible de restaurer les données: {e}"
            ) from e

    def clear(self) -> None:
        """
        Réinitialise les données aux valeurs par défaut
        """
        logger.warning(f"Réinitialisation des données de {self.file_path}")
        self.data = self._get_default_data()
        self.save()
