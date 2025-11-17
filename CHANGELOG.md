# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

## [0.2.0] - 2024-11-17

### Ajouté

**Tests et Qualité**
- Suite de tests unitaires complète (pytest)
- Configuration CI/CD avec GitHub Actions
- Pre-commit hooks (black, flake8, isort, mypy)
- Coverage de code
- Tests de sécurité (bandit)

**Gestion des Erreurs et Validation**
- Module de validation complet (`validators.py`)
- Exceptions personnalisées
- Système de logging structuré
- Validation des inputs utilisateurs
- Messages d'erreur clairs

**Templates de Politiques**
- Politique de développement sécurisé
- Politique de télétravail
- Politique de gestion des mots de passe
- Politique de sauvegarde et restauration

**Procédures Opérationnelles**
- Procédure de demande d'accès
- Procédure de réponse aux incidents

**Formulaires**
- Formulaire de demande d'accès
- Formulaire de déclaration d'incident

**Fonctionnalités CLI**
- Commande `search` : Recherche dans les contrôles
- Commande `export` : Export JSON/CSV (contrôles, risques)
- Commande `import` : Import de données
- Version bumped à 0.2.0

**Documentation**
- CHANGELOG.md
- CONTRIBUTING.md amélioré
- requirements-dev.txt
- Configuration pytest et CI/CD

### Amélioré
- CLI principal avec nouvelles commandes
- Architecture modulaire renforcée
- Gestion d'erreurs robuste
- Documentation code

## [0.1.0] - 2024-11-17

### Ajouté
- Version initiale
- CLI complet avec Click et Rich
- 11 templates de politiques ISO 27001
- Base de données des 114 contrôles ISO 27001:2022
- Gestion complète des risques
- Outils de préparation d'audit
- Templates Jinja2
- Configuration organisation
- README complet
- Licence MIT
