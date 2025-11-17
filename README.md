# ISO 27001 Toolkit

> Suite d'outils CLI Python open-source pour faciliter votre démarche de certification ISO 27001

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![ISO 27001:2022](https://img.shields.io/badge/ISO%2027001-2022-green.svg)](https://www.iso.org/standard/27001)

## 📋 Vue d'ensemble

**ISO 27001 Toolkit** est une suite complète d'outils en ligne de commande conçue pour accompagner les organisations dans leur démarche de certification ISO 27001:2022. Cet outil open-source facilite la génération de politiques, le suivi des 114 contrôles de l'Annexe A, la gestion des risques et la préparation des audits.

### ✨ Fonctionnalités principales

- **🔐 Génération de politiques de sécurité** : Templates Jinja2 personnalisables pour toutes les politiques ISO 27001
- **✅ Suivi des contrôles** : Gestion complète des 114 contrôles de l'Annexe A (ISO 27001:2022)
- **⚠️ Gestion des risques** : Identification, analyse et traitement des risques de sécurité
- **📊 Préparation d'audits** : Checklists, analyses d'écarts (gap analysis), génération de SOA
- **📄 Documentation automatisée** : Génération de rapports et documentation de conformité
- **🔒 Chiffrement des données sensibles** : Protection par chiffrement Fernet avec gestion de clés
- **✅ Validation robuste** : Validation stricte de toutes les entrées utilisateur
- **📝 Logging avancé** : Système de logs rotatifs pour le suivi et le débogage
- **🧪 Tests complets** : Suite de tests avec pytest pour assurer la qualité du code

## 🚀 Installation

### Pré-requis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation depuis PyPI (à venir)

```bash
pip install iso27001-toolkit
```

### Installation depuis les sources

```bash
# Cloner le repository
git clone https://github.com/GitCroque/iso27001-toolbox.git
cd iso27001-toolbox

# Installer les dépendances
pip install -r requirements.txt

# Installer le package
pip install -e .
```

## 📖 Guide de démarrage rapide

### 1. Configuration initiale

Configurez les informations de votre organisation :

```bash
iso27001 policies configure
```

Cette commande vous guidera à travers la configuration de :
- Nom de l'organisation
- Informations de contact (RSSI, DPO)
- Dates d'effet
- Période de révision

### 2. Génération des politiques

Générez toutes les politiques de sécurité :

```bash
iso27001 policies generate -o output/policies
```

Ou générez une politique spécifique :

```bash
iso27001 policies generate -p information_security_policy
```

### 3. Initialisation du suivi des contrôles

Initialisez le tracker des 114 contrôles ISO 27001:2022 :

```bash
iso27001 controls init
```

Listez tous les contrôles :

```bash
iso27001 controls list
```

Affichez le détail d'un contrôle :

```bash
iso27001 controls show A.5.1
```

### 4. Mise à jour des contrôles

Mettez à jour le statut d'un contrôle :

```bash
iso27001 controls update A.5.1 --status implemented --priority high
```

Ajoutez des preuves d'implémentation :

```bash
iso27001 controls update A.5.1 --evidence "Politique approuvée le 2024-01-15" --evidence "Formation dispensée"
```

### 5. Gestion des risques

Initialisez le registre des risques :

```bash
iso27001 risks init
```

Ajoutez un risque en mode interactif :

```bash
iso27001 risks add --interactive
```

Listez les risques par niveau :

```bash
iso27001 risks list --level high
```

Visualisez la matrice des risques :

```bash
iso27001 risks matrix
```

### 6. Préparation d'audit

Évaluez votre niveau de préparation :

```bash
iso27001 audit readiness
```

Générez une analyse des écarts :

```bash
iso27001 audit gap-analysis -o output/gap_analysis.md
```

Générez la Déclaration d'Applicabilité (SOA) :

```bash
iso27001 audit generate-soa -o output/soa.md
```

Préparez le package de preuves complet :

```bash
iso27001 audit prepare-evidence -o output/evidence_package
```

## 📚 Documentation complète

### Commandes disponibles

#### Politiques (`policies`)

```bash
iso27001 policies list                    # Liste toutes les politiques disponibles
iso27001 policies configure               # Configure l'organisation
iso27001 policies generate                # Génère toutes les politiques
iso27001 policies generate -p <name>      # Génère une politique spécifique
iso27001 policies generate -i             # Mode interactif
```

**Politiques disponibles :**
- `information_security_policy` - Politique générale de sécurité (A.5.1)
- `access_control_policy` - Politique de contrôle d'accès (A.5.15-18)
- `asset_management_policy` - Politique de gestion des actifs (A.5.9-14)
- `cryptography_policy` - Politique de cryptographie (A.8.24)
- `physical_security_policy` - Politique de sécurité physique (A.7.1-14)
- `operations_security_policy` - Politique de sécurité des opérations (A.8.1-34)
- `incident_management_policy` - Politique de gestion des incidents (A.5.24-28)
- `business_continuity_policy` - Politique de continuité d'activité (A.5.29-30)
- Et plus encore...

#### Contrôles (`controls`)

```bash
iso27001 controls init                    # Initialise le suivi des contrôles
iso27001 controls list                    # Liste tous les contrôles
iso27001 controls list -c A.5            # Filtre par catégorie
iso27001 controls list -s implemented    # Filtre par statut
iso27001 controls list -f summary        # Vue résumée par catégorie
iso27001 controls show <ID>              # Affiche le détail d'un contrôle
iso27001 controls update <ID> [options]  # Met à jour un contrôle
iso27001 controls report                 # Génère un rapport complet
```

**Statuts disponibles :**
- `not_started` - Non démarré
- `in_progress` - En cours d'implémentation
- `implemented` - Implémenté
- `verified` - Vérifié et validé

#### Risques (`risks`)

```bash
iso27001 risks init                      # Initialise le registre des risques
iso27001 risks list                      # Liste tous les risques
iso27001 risks list --level critical    # Filtre par niveau
iso27001 risks list --category conf     # Filtre par catégorie
iso27001 risks add -i                    # Ajoute un risque (interactif)
iso27001 risks show <ID>                # Affiche le détail d'un risque
iso27001 risks update <ID> [options]    # Met à jour un risque
iso27001 risks report                    # Génère un rapport d'évaluation
iso27001 risks matrix                    # Affiche la matrice des risques
```

**Niveaux de risque :**
- `low` - Risque faible (score 1-4)
- `medium` - Risque moyen (score 5-9)
- `high` - Risque élevé (score 10-15)
- `critical` - Risque critique (score 16-25)

#### Audit (`audit`)

```bash
iso27001 audit readiness                 # Évalue la préparation à l'audit
iso27001 audit checklist                 # Génère une checklist d'audit
iso27001 audit gap-analysis             # Effectue une analyse des écarts
iso27001 audit prepare-evidence         # Prépare le package de preuves
iso27001 audit generate-soa             # Génère la Déclaration d'Applicabilité
iso27001 audit schedule <date>          # Planifie un audit
```

## 🗂️ Structure des fichiers

```
~/.iso27001/
├── config.yml              # Configuration de l'organisation
└── data/
    ├── controls.yml        # État des contrôles
    ├── risks.yml          # Registre des risques
    └── audit.yml          # Données d'audit

output/                     # Fichiers générés
├── policies/              # Politiques générées
├── controls_report.md     # Rapport des contrôles
├── risk_assessment.md     # Évaluation des risques
├── gap_analysis.md        # Analyse des écarts
├── soa.md                # Déclaration d'Applicabilité
└── evidence_package/      # Package complet de preuves
```

## 🎯 Cas d'usage

### Scénario 1 : Démarrage d'une démarche ISO 27001

```bash
# 1. Configuration
iso27001 policies configure

# 2. Génération des politiques
iso27001 policies generate

# 3. Initialisation du suivi
iso27001 controls init
iso27001 risks init

# 4. Évaluation initiale
iso27001 audit gap-analysis
```

### Scénario 2 : Suivi de l'implémentation

```bash
# Mettre à jour les contrôles au fur et à mesure
iso27001 controls update A.5.1 --status implemented
iso27001 controls update A.5.2 --status in_progress

# Générer un rapport de progression
iso27001 controls report

# Visualiser l'état global
iso27001 controls list -f summary
```

### Scénario 3 : Préparation d'un audit de certification

```bash
# 1. Évaluer la préparation
iso27001 audit readiness

# 2. Générer l'analyse des écarts
iso27001 audit gap-analysis

# 3. Générer la SOA
iso27001 audit generate-soa

# 4. Préparer toutes les preuves
iso27001 audit prepare-evidence

# 5. Générer tous les rapports
iso27001 controls report
iso27001 risks report
```

## 🔧 Personnalisation

### Templates Jinja2

Tous les templates sont modifiables dans `src/iso27001_toolkit/templates/`. Vous pouvez les personnaliser selon vos besoins :

```
src/iso27001_toolkit/templates/
├── policies/
│   ├── information_security_policy.md
│   ├── access_control_policy.md
│   └── ...
├── risks/
│   └── risk_assessment.md
└── audit/
    └── checklist.md
```

### Variables disponibles dans les templates

- `organization_name` - Nom de l'organisation
- `organization_address` - Adresse
- `organization_city` - Ville
- `organization_country` - Pays
- `ciso_name` - Nom du RSSI
- `ciso_email` - Email du RSSI
- `dpo_name` - Nom du DPO
- `dpo_email` - Email du DPO
- `effective_date` - Date d'effet
- `review_period` - Période de révision
- `current_date` - Date de génération

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Pushez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

### Domaines où contribuer

- 📝 Ajout de nouveaux templates de politiques
- 🌍 Traductions (anglais, espagnol, etc.)
- 🔧 Nouvelles fonctionnalités CLI
- 📚 Amélioration de la documentation
- 🐛 Correction de bugs
- ✅ Tests unitaires

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 📞 Support

- 🐛 **Issues** : [GitHub Issues](https://github.com/GitCroque/iso27001-toolbox/issues)
- 💬 **Discussions** : [GitHub Discussions](https://github.com/GitCroque/iso27001-toolbox/discussions)
- 📧 **Email** : [contact]

## 🙏 Remerciements

- La norme ISO/IEC 27001:2022
- La communauté de la sécurité de l'information
- Tous les contributeurs du projet

## ⚠️ Avertissement

Cet outil est conçu pour faciliter la démarche de certification ISO 27001, mais ne garantit pas la certification. La conformité ISO 27001 nécessite une approche globale incluant :

- L'engagement de la direction
- L'analyse de contexte de l'organisation
- L'évaluation et le traitement des risques spécifiques
- L'implémentation effective des contrôles
- La surveillance et l'amélioration continue
- Un audit de certification par un organisme accrédité

## 🗺️ Roadmap

- [ ] Export des rapports en PDF
- [ ] Interface web de visualisation
- [ ] Intégration avec des outils de ticketing (Jira, etc.)
- [ ] Templates additionnels (procédures opérationnelles)
- [ ] Support multilingue complet
- [ ] Tableaux de bord interactifs
- [ ] API REST

## 📊 Statistiques

- **114 contrôles** ISO 27001:2022 (Annexe A)
- **11+ templates** de politiques
- **4 catégories** de contrôles (Organisationnels, Personnes, Physiques, Technologiques)
- **Python 3.8+** compatible

---

**Fait avec ❤️ pour la communauté de la sécurité de l'information**

*Aidez-nous à améliorer cet outil en le starred ⭐ sur GitHub !*
