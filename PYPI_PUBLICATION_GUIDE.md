# Guide de Publication sur PyPI

Guide complet pour publier iso27001-toolkit sur PyPI

## Pré-requis ✅

1. **Compte PyPI**
   - Créer un compte sur https://pypi.org/account/register/
   - Activer 2FA (Two-Factor Authentication) - **OBLIGATOIRE**
   - Créer un token API: https://pypi.org/manage/account/#api-tokens

2. **Outils installés**
   ```bash
   pip install build twine
   ```

## Étape 1: Préparation 📋

### 1.1 Vérifier la version

Modifier `src/iso27001_toolkit/__init__.py`:
```python
__version__ = "0.1.0"  # Incrémenter selon semver
```

### 1.2 Mettre à jour CHANGELOG.md

Documenter tous les changements de la nouvelle version:
```markdown
## [0.1.0] - 2025-11-18
### Added
- Tests de sécurité complets (37 tests)
- Audit trail (Who/When/What)
- Améliorations de sécurité dans validators
- Documentation SECURITY.md, ARCHITECTURE.md
...
```

### 1.3 Vérifier que tous les tests passent

```bash
pytest tests/ -v
# Doit afficher: All tests passed
```

## Étape 2: Build du Package 🔨

```bash
# Nettoyer les anciens builds
rm -rf dist/ build/ *.egg-info

# Créer le package
python -m build

# Vérifier le contenu
tar -tzf dist/iso27001-toolkit-*.tar.gz | head -20
```

### Fichiers créés:
- `dist/iso27001_toolkit-0.1.0-py3-none-any.whl` (wheel, 85KB)
- `dist/iso27001_toolkit-0.1.0.tar.gz` (source dist, 95KB)

## Étape 3: Vérifications Qualité ✨

### 3.1 Vérifier avec twine

```bash
twine check dist/*
```

Sortie attendue: ✅ `PASSED` pour tous les fichiers

### 3.2 Tester l'installation locale

```bash
# Créer un environnement virtuel de test
python -m venv test_env
source test_env/bin/activate

# Installer depuis le wheel
pip install dist/iso27001_toolkit-0.1.0-py3-none-any.whl

# Tester la commande
iso27001 --help

# Vérifier que les templates sont inclus
python -c "from iso27001_toolkit.utils.template_engine import TemplateEngine; print(TemplateEngine().template_dir)"

# Désactiver l'env
deactivate
rm -rf test_env
```

## Étape 4: Publication sur TestPyPI (Recommandé) 🧪

TestPyPI permet de tester la publication sans affecter PyPI production.

### 4.1 Créer un compte TestPyPI

- https://test.pypi.org/account/register/
- Créer un token API

### 4.2 Publier sur TestPyPI

```bash
twine upload --repository testpypi dist/*
# Username: __token__
# Password: <votre-token-testpypi>
```

### 4.3 Tester l'installation depuis TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ iso27001-toolkit
```

Si tout fonctionne, passer à l'étape suivante.

## Étape 5: Publication sur PyPI Production 🚀

### 5.1 Upload sur PyPI

```bash
twine upload dist/*
# Username: __token__
# Password: <votre-token-pypi>
```

### 5.2 Vérifier la publication

- Visiter: https://pypi.org/project/iso27001-toolkit/
- Vérifier que README s'affiche correctement
- Vérifier les métadonnées (licence, classifiers, etc.)

## Étape 6: Post-Publication 📢

### 6.1 Tester l'installation

```bash
pip install iso27001-toolkit
iso27001 --version  # Doit afficher: 0.1.0
```

### 6.2 Créer un tag Git

```bash
git tag -a v0.1.0 -m "Release v0.1.0 - First PyPI release"
git push origin v0.1.0
```

### 6.3 Créer une GitHub Release

1. Aller sur https://github.com/VOTRE-USER/iso27001-toolbox/releases/new
2. Tag version: `v0.1.0`
3. Release title: `v0.1.0 - First PyPI Release`
4. Description: Copier depuis CHANGELOG.md
5. Attacher les fichiers `dist/*`
6. Publier

### 6.4 Annoncer la release

- Mettre à jour README.md avec badge PyPI:
  ```markdown
  ![PyPI](https://img.shields.io/pypi/v/iso27001-toolkit)
  ![Downloads](https://img.shields.io/pypi/dm/iso27001-toolkit)
  ```
- Twitter/LinkedIn/Reddit (r/netsec, r/ISO27001)
- Blog post

## Configuration Automatique (CI/CD) 🤖

### GitHub Actions pour auto-publication

Créer `.github/workflows/publish-pypi.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine
      - name: Build package
        run: python -m build
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

Ajouter le token PyPI dans GitHub Secrets: `PYPI_API_TOKEN`

## Versions Suivantes 📦

Pour publier une nouvelle version:

1. Mettre à jour `__version__`
2. Mettre à jour CHANGELOG.md
3. Commit et push
4. Créer un tag: `git tag v0.2.0 && git push --tags`
5. Créer une GitHub Release → CI/CD publish automatiquement

## Troubleshooting 🔧

### Erreur: "File already exists"

Le package existe déjà pour cette version. Incrémenter la version.

### Erreur: "Invalid distribution"

Vérifier avec `twine check dist/*`

### Templates non inclus

Vérifier `MANIFEST.in` et rebuilder.

### Dépendances manquantes

Vérifier `pyproject.toml` section `dependencies`.

## Ressources 📚

- PyPI Help: https://pypi.org/help/
- Packaging Guide: https://packaging.python.org/
- Semver: https://semver.org/
- twine docs: https://twine.readthedocs.io/

---

**Prêt à publier ! 🎉**
