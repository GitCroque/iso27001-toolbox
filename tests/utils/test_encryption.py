"""
Tests pour le module de chiffrement
"""

import pytest
from pathlib import Path

try:
    from iso27001_toolkit.utils.encryption import EncryptionManager
    from iso27001_toolkit.exceptions import EncryptionError
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False


@pytest.mark.skipif(not CRYPTOGRAPHY_AVAILABLE, reason="cryptography not installed")
class TestEncryptionManager:
    """Tests pour EncryptionManager"""

    def test_initialization(self, encryption_key_file):
        """Test l'initialisation du gestionnaire"""
        manager = EncryptionManager(key_file=encryption_key_file)
        assert manager.key_file == encryption_key_file
        assert encryption_key_file.exists()

    def test_encrypt_decrypt_string(self, encryption_key_file):
        """Test le chiffrement et déchiffrement d'une chaîne"""
        manager = EncryptionManager(key_file=encryption_key_file)

        original = "Données sensibles ISO 27001"
        encrypted = manager.encrypt(original)

        # Les données chiffrées doivent être différentes
        assert encrypted != original

        # Déchiffrer doit retourner l'original
        decrypted = manager.decrypt(encrypted)
        assert decrypted == original

    def test_encrypt_decrypt_bytes(self, encryption_key_file):
        """Test le chiffrement de bytes"""
        manager = EncryptionManager(key_file=encryption_key_file)

        original = b"Binary data"
        encrypted = manager.encrypt(original)
        decrypted = manager.decrypt(encrypted)

        assert decrypted == original.decode('utf-8')

    def test_encrypt_file(self, encryption_key_file, temp_dir):
        """Test le chiffrement de fichier"""
        manager = EncryptionManager(key_file=encryption_key_file)

        # Créer un fichier test
        test_file = temp_dir / "test.txt"
        test_content = "Contenu confidentiel"
        test_file.write_text(test_content)

        # Chiffrer le fichier
        encrypted_file = manager.encrypt_file(test_file)
        assert encrypted_file.exists()
        assert encrypted_file != test_file

        # Le contenu chiffré doit être différent
        encrypted_content = encrypted_file.read_bytes()
        assert encrypted_content != test_content.encode('utf-8')

    def test_decrypt_file(self, encryption_key_file, temp_dir):
        """Test le déchiffrement de fichier"""
        manager = EncryptionManager(key_file=encryption_key_file)

        # Créer et chiffrer un fichier
        test_file = temp_dir / "test.txt"
        test_content = "Contenu à protéger"
        test_file.write_text(test_content)

        encrypted_file = manager.encrypt_file(test_file)

        # Déchiffrer
        decrypted_file = manager.decrypt_file(encrypted_file)
        assert decrypted_file.exists()

        # Vérifier le contenu
        decrypted_content = decrypted_file.read_text()
        assert decrypted_content == test_content

    def test_decrypt_with_wrong_key_fails(self, temp_dir):
        """Test que le déchiffrement avec une mauvaise clé échoue"""
        key_file1 = temp_dir / "key1.key"
        key_file2 = temp_dir / "key2.key"

        manager1 = EncryptionManager(key_file=key_file1)
        manager2 = EncryptionManager(key_file=key_file2)

        original = "Secret data"
        encrypted = manager1.encrypt(original)

        # Déchiffrer avec une autre clé devrait échouer
        with pytest.raises(EncryptionError):
            manager2.decrypt(encrypted)

    def test_key_persistence(self, encryption_key_file):
        """Test que la clé est conservée entre les instances"""
        manager1 = EncryptionManager(key_file=encryption_key_file)
        original = "Test data"
        encrypted = manager1.encrypt(original)

        # Créer une nouvelle instance avec le même fichier clé
        manager2 = EncryptionManager(key_file=encryption_key_file)
        decrypted = manager2.decrypt(encrypted)

        assert decrypted == original
