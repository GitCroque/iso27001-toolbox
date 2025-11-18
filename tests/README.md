# Tests ISO 27001 Toolkit

Ce répertoire contient les tests pour le projet ISO 27001 Toolkit.

## Structure

```
tests/
├── conftest.py              # Fixtures partagées
├── test_cli.py             # Tests du CLI principal
├── utils/                  # Tests des modules utilitaires
│   ├── test_validators.py  # Tests de validation
│   ├── test_encryption.py  # Tests de chiffrement
│   └── test_base_storage.py # Tests de stockage YAML
└── commands/               # Tests des commandes CLI
```

## Exécuter les tests

### Tous les tests

```bash
pytest
```

### Tests avec couverture

```bash
pytest --cov=iso27001_toolkit --cov-report=html
```

### Tests spécifiques

```bash
# Un fichier de test
pytest tests/utils/test_validators.py

# Un test spécifique
pytest tests/utils/test_validators.py::TestValidateEmail::test_valid_email

# Tests par catégorie
pytest -m unit  # Tests unitaires uniquement
pytest -m integration  # Tests d'intégration uniquement
```

### Tests en mode verbeux

```bash
pytest -v
```

### Tests avec sortie détaillée

```bash
pytest -vv
```

## Fixtures disponibles

Les fixtures suivantes sont disponibles dans `conftest.py` :

- `temp_dir` : Répertoire temporaire pour les tests
- `mock_config_dir` : Mock du répertoire de configuration
- `mock_data_dir` : Mock du répertoire de données
- `sample_organization_config` : Configuration d'organisation pour les tests
- `sample_risk_data` : Données de risque pour les tests
- `sample_control_data` : Données de contrôle pour les tests
- `mock_console` : Mock Rich console pour les tests CLI
- `encryption_key_file` : Fichier de clé de chiffrement temporaire

## Ajouter de nouveaux tests

### Structure d'un test

```python
import pytest
from iso27001_toolkit.module import function_to_test

class TestMyFunction:
    """Tests pour my_function"""

    def test_basic_case(self):
        """Test le cas de base"""
        result = function_to_test("input")
        assert result == "expected"

    def test_edge_case(self):
        """Test un cas limite"""
        with pytest.raises(ValueError):
            function_to_test(None)
```

### Utiliser les fixtures

```python
def test_with_fixture(temp_dir):
    """Test utilisant une fixture"""
    test_file = temp_dir / "test.txt"
    test_file.write_text("content")
    assert test_file.exists()
```

## Bonnes pratiques

1. **Nommer les tests clairement** : Utilisez des noms descriptifs
2. **Un test, un comportement** : Chaque test doit vérifier un seul comportement
3. **Utiliser des fixtures** : Évitez la duplication de code de configuration
4. **Tester les cas limites** : Incluez les cas d'erreur et les valeurs extrêmes
5. **Isolation** : Les tests ne doivent pas dépendre les uns des autres
6. **Documentation** : Ajoutez des docstrings pour expliquer ce que teste chaque test

## Couverture de code

L'objectif est d'atteindre une couverture de code d'au moins 80%.

Pour générer un rapport de couverture :

```bash
pytest --cov=iso27001_toolkit --cov-report=html
open htmlcov/index.html  # Sur macOS/Linux
```

## CI/CD

Les tests sont exécutés automatiquement via CI/CD sur chaque push et pull request.
