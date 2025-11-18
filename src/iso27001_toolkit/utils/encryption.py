"""
Module de chiffrement pour les données sensibles
"""

import os
from pathlib import Path
from typing import Union

from iso27001_toolkit.exceptions import EncryptionError
from iso27001_toolkit.logger import get_logger

logger = get_logger(__name__)


class EncryptionManager:
    """
    Gestionnaire de chiffrement pour les données sensibles

    Utilise Fernet (chiffrement symétrique) de la bibliothèque cryptography
    """

    def __init__(self, key_file: Path = None):
        """
        Initialise le gestionnaire de chiffrement

        Args:
            key_file: Chemin du fichier contenant la clé de chiffrement
                     (défaut: ~/.iso27001/encryption.key)

        Raises:
            EncryptionError: Si l'initialisation échoue
        """
        try:
            from cryptography.fernet import Fernet
            self.Fernet = Fernet
        except ImportError as e:
            raise EncryptionError(
                "La bibliothèque 'cryptography' n'est pas installée. "
                "Installez-la avec: pip install cryptography"
            ) from e

        if key_file is None:
            key_file = Path.home() / ".iso27001" / "encryption.key"

        self.key_file = key_file
        self.key = self._load_or_generate_key()
        self.cipher = self.Fernet(self.key)

        logger.debug(f"Gestionnaire de chiffrement initialisé avec clé: {self.key_file}")

    def _load_or_generate_key(self) -> bytes:
        """
        Charge la clé de chiffrement ou en génère une nouvelle

        Returns:
            Clé de chiffrement

        Raises:
            EncryptionError: Si le chargement ou la génération échoue
        """
        if self.key_file.exists():
            try:
                with open(self.key_file, 'rb') as f:
                    key = f.read()
                    logger.debug("Clé de chiffrement chargée")
                    return key
            except Exception as e:
                logger.error(f"Erreur lors du chargement de la clé: {e}")
                raise EncryptionError(
                    f"Impossible de charger la clé de chiffrement: {e}"
                ) from e
        else:
            return self._generate_key()

    def _generate_key(self) -> bytes:
        """
        Génère une nouvelle clé de chiffrement et la sauvegarde

        Returns:
            Nouvelle clé de chiffrement

        Raises:
            EncryptionError: Si la génération ou la sauvegarde échoue
        """
        try:
            key = self.Fernet.generate_key()

            # Créer le répertoire parent si nécessaire
            self.key_file.parent.mkdir(parents=True, exist_ok=True)

            # Sauvegarder la clé avec permissions restrictives
            with open(self.key_file, 'wb') as f:
                f.write(key)

            # Définir les permissions (lecture/écriture pour l'utilisateur seulement)
            os.chmod(self.key_file, 0o600)

            logger.info(f"Nouvelle clé de chiffrement générée: {self.key_file}")
            logger.warning(
                "⚠️  IMPORTANT: Sauvegardez cette clé en lieu sûr! "
                "Sans elle, vous ne pourrez pas déchiffrer vos données."
            )

            return key

        except Exception as e:
            logger.error(f"Erreur lors de la génération de la clé: {e}")
            raise EncryptionError(
                f"Impossible de générer la clé de chiffrement: {e}"
            ) from e

    def encrypt(self, data: Union[str, bytes]) -> str:
        """
        Chiffre des données

        Args:
            data: Données à chiffrer (str ou bytes)

        Returns:
            Données chiffrées encodées en base64 (str)

        Raises:
            EncryptionError: Si le chiffrement échoue
        """
        try:
            # Convertir en bytes si nécessaire
            if isinstance(data, str):
                data = data.encode('utf-8')

            # Chiffrer
            encrypted = self.cipher.encrypt(data)

            # Retourner en tant que string (base64)
            return encrypted.decode('utf-8')

        except Exception as e:
            logger.error(f"Erreur lors du chiffrement: {e}")
            raise EncryptionError(f"Impossible de chiffrer les données: {e}") from e

    def decrypt(self, encrypted_data: Union[str, bytes]) -> str:
        """
        Déchiffre des données

        Args:
            encrypted_data: Données chiffrées (str en base64 ou bytes)

        Returns:
            Données déchiffrées (str)

        Raises:
            EncryptionError: Si le déchiffrement échoue
        """
        try:
            # Convertir en bytes si nécessaire
            if isinstance(encrypted_data, str):
                encrypted_data = encrypted_data.encode('utf-8')

            # Déchiffrer
            decrypted = self.cipher.decrypt(encrypted_data)

            # Retourner en tant que string
            return decrypted.decode('utf-8')

        except Exception as e:
            logger.error(f"Erreur lors du déchiffrement: {e}")
            raise EncryptionError(
                f"Impossible de déchiffrer les données. "
                f"Vérifiez que vous utilisez la bonne clé de chiffrement. "
                f"Erreur: {e}"
            ) from e

    def encrypt_file(self, input_file: Path, output_file: Path = None) -> Path:
        """
        Chiffre un fichier

        Args:
            input_file: Fichier à chiffrer
            output_file: Fichier de sortie (défaut: input_file.encrypted)

        Returns:
            Chemin du fichier chiffré

        Raises:
            EncryptionError: Si le chiffrement échoue
        """
        if not input_file.exists():
            raise EncryptionError(f"Fichier source n'existe pas: {input_file}")

        if output_file is None:
            output_file = input_file.with_suffix(input_file.suffix + '.encrypted')

        try:
            with open(input_file, 'rb') as f:
                data = f.read()

            encrypted = self.cipher.encrypt(data)

            with open(output_file, 'wb') as f:
                f.write(encrypted)

            logger.info(f"Fichier chiffré: {input_file} -> {output_file}")
            return output_file

        except Exception as e:
            logger.error(f"Erreur lors du chiffrement du fichier: {e}")
            raise EncryptionError(
                f"Impossible de chiffrer le fichier {input_file}: {e}"
            ) from e

    def decrypt_file(self, input_file: Path, output_file: Path = None) -> Path:
        """
        Déchiffre un fichier

        Args:
            input_file: Fichier chiffré
            output_file: Fichier de sortie (défaut: supprime .encrypted)

        Returns:
            Chemin du fichier déchiffré

        Raises:
            EncryptionError: Si le déchiffrement échoue
        """
        if not input_file.exists():
            raise EncryptionError(f"Fichier source n'existe pas: {input_file}")

        if output_file is None:
            if input_file.suffix == '.encrypted':
                output_file = input_file.with_suffix('')
            else:
                output_file = input_file.with_suffix('.decrypted')

        try:
            with open(input_file, 'rb') as f:
                encrypted_data = f.read()

            decrypted = self.cipher.decrypt(encrypted_data)

            with open(output_file, 'wb') as f:
                f.write(decrypted)

            logger.info(f"Fichier déchiffré: {input_file} -> {output_file}")
            return output_file

        except Exception as e:
            logger.error(f"Erreur lors du déchiffrement du fichier: {e}")
            raise EncryptionError(
                f"Impossible de déchiffrer le fichier {input_file}: {e}"
            ) from e

    def rotate_key(self, new_key_file: Path = None) -> None:
        """
        Rotation de la clé de chiffrement

        ATTENTION: Cette opération nécessite de re-chiffrer toutes les données
        avec la nouvelle clé

        Args:
            new_key_file: Chemin pour la nouvelle clé (défaut: même emplacement)

        Raises:
            EncryptionError: Si la rotation échoue
        """
        logger.warning("⚠️  Rotation de clé demandée - opération sensible")

        try:
            # Générer une nouvelle clé
            new_key = self.Fernet.generate_key()

            # Sauvegarder l'ancienne clé
            backup_key_file = self.key_file.with_suffix('.key.backup')
            import shutil
            shutil.copy2(self.key_file, backup_key_file)

            # Sauvegarder la nouvelle clé
            if new_key_file is None:
                new_key_file = self.key_file

            with open(new_key_file, 'wb') as f:
                f.write(new_key)

            os.chmod(new_key_file, 0o600)

            logger.info(
                f"Nouvelle clé générée. "
                f"Ancienne clé sauvegardée: {backup_key_file}"
            )
            logger.warning(
                "⚠️  IMPORTANT: Vous devez re-chiffrer toutes vos données "
                "avec la nouvelle clé!"
            )

        except Exception as e:
            logger.error(f"Erreur lors de la rotation de clé: {e}")
            raise EncryptionError(f"Impossible de faire la rotation de clé: {e}") from e
