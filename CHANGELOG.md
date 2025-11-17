# Changelog

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [0.2.0] - 2025-11-17

### Ajouté

#### Sécurité et Validation
- **Module de validation** (`validators.py`) pour valider toutes les entrées utilisateur
  - Validation d'emails, dates, URLs, chemins de fichiers
  - Validation des scores de risques et pourcentages
  - Validation des IDs de contrôles ISO 27001
  - Sanitisation des noms de fichiers
- **Module de chiffrement** (`utils/encryption.py`) pour protéger les données sensibles
  - Chiffrement symétrique avec Fernet
  - Chiffrement/déchiffrement de fichiers et de chaînes
  - Gestion sécurisée des clés de chiffrement
  - Rotation de clés

#### Qualité du Code
- **Exceptions personnalisées** (`exceptions.py`) pour une meilleure gestion des erreurs
  - `ConfigurationError`, `ValidationError`, `TemplateError`
  - `DataPersistenceError`, `EncryptionError`, `AuditError`
  - Classes spécifiques pour chaque type d'erreur
- **Système de logging** (`logger.py`) centralisé
  - Logs rotatifs (5 fichiers de 5 MB)
  - Niveaux de log configurables
  - Stockage dans `~/.iso27001/logs/`
- **Constantes centralisées** (`constants.py`)
  - Toutes les valeurs magiques sont maintenant des constantes nommées
  - Facilite la maintenance et la compréhension du code
- **Classe de base pour le stockage YAML** (`utils/base_storage.py`)
  - Élimine la duplication de code
  - Fonctionnalités de backup et restore
  - Support du chiffrement optionnel

#### Fonctionnalités
- **Templates manquants** complétés
  - `templates/risks/risk_assessment.md` - Rapport d'évaluation des risques
  - `templates/audit/checklist.md` - Checklist d'audit complète
  - `templates/audit/gap_analysis.md` - Analyse détaillée des écarts
- **Copie des politiques dans audit_helper** implémentée
  - Collection automatique des politiques générées
  - Rapport des politiques manquantes
  - Index markdown avec statut de chaque politique

#### Tests
- **Suite de tests complète** avec pytest
  - Tests unitaires pour validators, encryption, base_storage
  - Tests d'intégration pour le CLI
  - Fixtures partagées dans conftest.py
  - Documentation des tests dans tests/README.md
  - Configuration pytest dans pyproject.toml

### Modifié

#### Améliorations Techniques
- **Gestion des versions centralisée**
  - Version unique dans `__init__.py`
  - `setup.py` et `pyproject.toml` lisent depuis `__init__.py`
  - Pas de duplication de la version
- **Cohérence du code**
  - Utilisation exclusive de `console.print()` au lieu de `print()`
  - Remplacement des magic numbers par des constantes
  - Code plus lisible et maintenable

#### Dépendances
- Ajout de `cryptography>=41.0.0` pour le chiffrement

### Corrigé
- Mélange de `print()` et `console.print()` dans risks.py
- TODO incomplet pour la copie des politiques dans audit_helper.py
- Absence de templates pour les risques et l'audit
- Manque de validation des entrées utilisateur

### Sécurité
- Les données sensibles peuvent maintenant être chiffrées
- Validation stricte de toutes les entrées utilisateur
- Logs sécurisés avec rotation automatique
- Gestion appropriée des permissions de fichiers pour les clés

## [0.1.0] - 2025-11-17

### Ajouté
- Version initiale du toolkit ISO 27001
- Génération de 11 politiques de sécurité
- Suivi des 114 contrôles ISO 27001:2022
- Gestion complète des risques
- Préparation d'audits
- CLI avec Click
- Interface Rich pour l'affichage
- Templates Jinja2 pour les politiques

---

## Légende

- **Ajouté** : Nouvelles fonctionnalités
- **Modifié** : Changements dans les fonctionnalités existantes
- **Déprécié** : Fonctionnalités bientôt supprimées
- **Supprimé** : Fonctionnalités supprimées
- **Corrigé** : Corrections de bugs
- **Sécurité** : Corrections de vulnérabilités
