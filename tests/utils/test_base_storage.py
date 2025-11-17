"""
Tests pour le module base_storage
"""

import pytest
import yaml
from pathlib import Path

from iso27001_toolkit.utils.base_storage import YAMLStorage
from iso27001_toolkit.exceptions import DataPersistenceError


class TestYAMLStorage:
    """Tests pour la classe YAMLStorage"""

    def test_initialization(self, temp_dir):
        """Test l'initialisation"""
        file_path = temp_dir / "test.yml"
        storage = YAMLStorage(file_path)

        assert storage.file_path == file_path
        assert storage.encrypt == False
        assert storage.data == {}

    def test_load_nonexistent_file(self, temp_dir):
        """Test le chargement d'un fichier qui n'existe pas"""
        file_path = temp_dir / "nonexistent.yml"
        storage = YAMLStorage(file_path)

        data = storage.load()
        assert data == {'last_updated': None}

    def test_save_and_load(self, temp_dir):
        """Test la sauvegarde et le chargement"""
        file_path = temp_dir / "test.yml"
        storage = YAMLStorage(file_path)

        storage.data = {
            'test_key': 'test_value',
            'nested': {'key': 'value'}
        }
        storage.save()

        # Vérifier que le fichier existe
        assert file_path.exists()

        # Charger dans une nouvelle instance
        storage2 = YAMLStorage(file_path)
        data = storage2.load()

        assert data['test_key'] == 'test_value'
        assert data['nested']['key'] == 'value'
        assert 'last_updated' in data

    def test_backup(self, temp_dir):
        """Test la création de sauvegarde"""
        file_path = temp_dir / "test.yml"
        storage = YAMLStorage(file_path)

        storage.data = {'key': 'value'}
        storage.save()

        # Créer une sauvegarde
        backup_path = storage.backup()

        assert backup_path.exists()
        assert backup_path != file_path

        # Vérifier que le contenu est identique
        with open(backup_path, 'r') as f:
            backup_data = yaml.safe_load(f)
        assert backup_data['key'] == 'value'

    def test_restore(self, temp_dir):
        """Test la restauration depuis une sauvegarde"""
        file_path = temp_dir / "test.yml"
        backup_path = temp_dir / "backup.yml"

        # Créer une sauvegarde
        backup_data = {'restored': True, 'last_updated': None}
        with open(backup_path, 'w') as f:
            yaml.dump(backup_data, f)

        # Restaurer
        storage = YAMLStorage(file_path)
        storage.restore(backup_path)

        assert storage.data['restored'] == True

    def test_clear(self, temp_dir):
        """Test la réinitialisation des données"""
        file_path = temp_dir / "test.yml"
        storage = YAMLStorage(file_path)

        storage.data = {'key': 'value', 'other': 'data'}
        storage.save()

        # Réinitialiser
        storage.clear()

        assert storage.data == {'last_updated': None}
        assert file_path.exists()  # Le fichier devrait toujours exister après clear

    def test_invalid_yaml(self, temp_dir):
        """Test la gestion d'un YAML invalide"""
        file_path = temp_dir / "invalid.yml"

        # Créer un fichier YAML invalide
        file_path.write_text("invalid: yaml: content: :")

        storage = YAMLStorage(file_path)

        with pytest.raises(DataPersistenceError):
            storage.load()
