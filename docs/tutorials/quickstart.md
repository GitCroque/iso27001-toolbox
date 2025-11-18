# 🚀 Démarrage Rapide - ISO 27001 Toolkit

**Durée estimée : 30 minutes**

Ce guide vous accompagne pas à pas pour créer votre premier projet de certification ISO 27001.

## 📋 Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- 30 minutes de temps disponible

## 📦 Étape 1 : Installation (2 min)

Installez le toolkit via PyPI :

```bash
pip install iso27001-toolkit
```

Vérifiez l'installation :

```bash
iso27001 --version
```

Vous devriez voir : `ISO 27001 Toolkit, version 0.1.0`

## 🏗️ Étape 2 : Initialisation du Projet (3 min)

Créez un nouveau répertoire pour votre projet :

```bash
mkdir mon-projet-iso27001
cd mon-projet-iso27001
```

Initialisez le projet :

```bash
iso27001 init
```

Le système va vous poser quelques questions :

```
Nom de l'organisation : MonEntreprise SAS
Description : Éditeur de logiciel SaaS de gestion de projets
Secteur d'activité : Technologie
Nombre d'employés : 45
```

✅ **Résultat** : Un répertoire `.iso27001/` a été créé avec la structure suivante :
- `organization.yml` - Informations de votre organisation
- `risks.yml` - Registre des risques (vide pour l'instant)
- `controls.yml` - Suivi des 114 contrôles ISO 27001:2022
- `audit_trail.yml` - Journal d'audit de toutes vos actions
- `encryption.key` - Clé de chiffrement pour données sensibles

## 🎯 Étape 3 : Diagnostic de Santé (1 min)

Vérifiez que tout est bien configuré :

```bash
iso27001 doctor
```

Vous devriez voir un score de santé > 90% avec :
- ✓ Répertoire de configuration créé
- ✓ Fichiers de données présents
- ✓ Permissions sécurisées (0600)
- ✓ Clé de chiffrement générée

## ⚠️ Étape 4 : Ajouter 5 Risques (8 min)

Identifions et enregistrons 5 risques typiques pour notre entreprise SaaS.

### Risque 1 : Perte de données client

```bash
iso27001 risk add
```

Répondez aux questions :

```
Titre : Perte de données client suite à défaillance serveur
Description : Les données clients pourraient être perdues en cas de défaillance matérielle des serveurs
Probabilité (1-5) : 3
Impact (1-5) : 5
Catégorie : Technique
```

### Risque 2 : Accès non autorisé

```bash
iso27001 risk add
```

```
Titre : Accès non autorisé aux données sensibles
Description : Un employé pourrait accéder à des données clients sans autorisation légitime
Probabilité (1-5) : 4
Impact (1-5) : 4
Catégorie : Humain
```

### Risque 3 : Ransomware

```bash
iso27001 risk add
```

```
Titre : Infection par ransomware
Description : Les systèmes pourraient être infectés par un ransomware via email de phishing
Probabilité (1-5) : 3
Impact (1-5) : 5
Catégorie : Cyber-sécurité
```

### Risque 4 : Départ de personnel clé

```bash
iso27001 risk add
```

```
Titre : Départ du RSSI avec connaissances critiques
Description : Le RSSI pourrait quitter l'entreprise en emportant des connaissances non documentées
Probabilité (1-5) : 2
Impact (1-5) : 4
Catégorie : Organisationnel
```

### Risque 5 : Non-conformité RGPD

```bash
iso27001 risk add
```

```
Titre : Non-conformité RGPD sur traitement données
Description : Les procédures de traitement des données pourraient ne pas être conformes au RGPD
Probabilité (1-5) : 3
Impact (1-5) : 4
Catégorie : Légal
```

### Visualiser vos risques

```bash
iso27001 risk list
```

Vous verrez une matrice des risques avec les 5 risques classés par niveau (Critique, Élevé, Moyen, Faible).

**💡 Astuce** : Les risques avec un score ≥ 15 sont critiques et doivent être traités en priorité.

## 🛡️ Étape 5 : Implémenter 10 Contrôles (10 min)

Sélectionnons 10 contrôles parmi les 114 de l'ISO 27001:2022 et marquons-les comme implémentés.

### Contrôle 1 : A.5.1 - Politiques de sécurité

```bash
iso27001 control update A.5.1
```

```
Nouveau statut (not_started/in_progress/implemented/verified) : implemented
Notes de mise en œuvre : Politique de sécurité de l'information approuvée par la direction le 15/11/2025
```

### Contrôle 2 : A.5.2 - Rôles et responsabilités

```bash
iso27001 control update A.5.2
```

```
Statut : implemented
Notes : RSSI nommé (Jean Dupont), matrice RACI documentée dans l'organigramme
```

### Contrôle 3 : A.5.10 - Utilisation acceptable des actifs

```bash
iso27001 control update A.5.10
```

```
Statut : implemented
Notes : Charte d'utilisation des ressources informatiques signée par tous les employés (45/45)
```

### Contrôle 4 : A.8.2 - Droits d'accès privilégiés

```bash
iso27001 control update A.8.2
```

```
Statut : implemented
Notes : Liste des comptes admin documentée, revue trimestrielle en place depuis Q1 2025
```

### Contrôle 5 : A.8.3 - Restriction des accès

```bash
iso27001 control update A.8.3
```

```
Statut : implemented
Notes : Principe du moindre privilège appliqué via Azure AD avec RBAC
```

### Contrôle 6 : A.5.23 - Sécurité dans l'utilisation des services cloud

```bash
iso27001 control update A.5.23
```

```
Statut : in_progress
Notes : Migration vers AWS en cours, contrat DPA signé, chiffrement activé (70% migré)
```

### Contrôle 7 : A.8.5 - Authentification sécurisée

```bash
iso27001 control update A.8.5
```

```
Statut : implemented
Notes : MFA obligatoire pour tous les comptes (Duo Security), taux d'adoption 100%
```

### Contrôle 8 : A.8.8 - Gestion des secrets techniques

```bash
iso27001 control update A.8.8
```

```
Statut : implemented
Notes : Utilisation de HashiCorp Vault pour tous les secrets, rotation automatique 90j
```

### Contrôle 9 : A.8.10 - Suppression d'informations

```bash
iso27001 control update A.8.10
```

```
Statut : implemented
Notes : Procédure de suppression sécurisée documentée, utilisation de shred/wipe
```

### Contrôle 10 : A.8.23 - Filtrage Web

```bash
iso27001 control update A.8.23
```

```
Statut : implemented
Notes : Proxy Squid avec liste noire CrowdSec, logs conservés 12 mois
```

### Visualiser vos contrôles

```bash
iso27001 control list --status all
```

Vous verrez les 114 contrôles avec :
- ✓ 9 contrôles implémentés (implemented)
- 🔄 1 contrôle en cours (in_progress)
- 104 contrôles non démarrés (not_started)

**Taux d'implémentation : ~8%** (10/114 contrôles traités)

## 📊 Étape 6 : Générer les Rapports d'Audit (5 min)

Générons les 4 rapports essentiels pour un audit ISO 27001.

### 1. Registre des Risques

```bash
iso27001 audit risk-register
```

✅ Fichier généré : `risk_register_20251118.md`

Ce rapport contient :
- Matrice des risques (visualisation)
- Liste détaillée des 5 risques
- Traitements recommandés

### 2. Statement of Applicability (SoA)

```bash
iso27001 audit soa
```

✅ Fichier généré : `soa_20251118.md`

Le SoA montre :
- Les 114 contrôles ISO 27001:2022
- Statut de chaque contrôle (implémenté / en cours / non démarré)
- Justifications pour chaque contrôle

### 3. Évaluation de Maturité

```bash
iso27001 audit assess
```

✅ Fichier généré : `assessment_20251118.md`

L'évaluation affiche :
- Score global de maturité : ~8%
- Répartition par domaine (A.5, A.6, A.7, A.8)
- Recommandations pour améliorer le score

### 4. Checklist d'Audit

```bash
iso27001 audit checklist
```

✅ Fichier généré : `audit_checklist_20251118.md`

La checklist contient :
- Questions pour chaque contrôle
- Statut actuel
- Preuves attendues par les auditeurs

### Visualiser le Dashboard Complet

```bash
iso27001 dashboard
```

Vous obtenez une vue consolidée :

```
📊 ISO 27001 Dashboard

📈 Vue d'ensemble
  Contrôles implémentés : 9/114 (8%)
  Contrôles vérifiés : 0/114 (0%)

⚠️  Risques
  Critiques : 2
  Élevés : 3
  Moyens : 0
  Faibles : 0
  Total : 5 risques

📋 Top 5 Priorités
  1. [CRITIQUE] Perte de données client (score: 15)
  2. [CRITIQUE] Infection par ransomware (score: 15)
  3. [ÉLEVÉ] Accès non autorisé (score: 16)
  4. [ÉLEVÉ] Non-conformité RGPD (score: 12)
  5. [MOYEN] Départ du RSSI (score: 8)
```

## 🎓 Étape 7 : Consulter l'Audit Trail (1 min)

Toutes vos actions ont été enregistrées automatiquement. Consultez l'historique :

```bash
iso27001 audit trail --limit 20
```

Vous verrez :
- 🕐 Horodatage de chaque action
- 👤 Utilisateur qui a effectué l'action
- 📝 Type d'action (risk_created, control_updated, etc.)
- ✅ Succès ou échec de l'opération

**Exemple de sortie :**

```
=== Audit Trail (20 dernières entrées) ===

[2025-11-18 14:32:15] user@hostname
  Action: control_status_updated
  Entity: control:A.8.23
  Details: status changed to implemented
  ✅ Success

[2025-11-18 14:30:42] user@hostname
  Action: risk_created
  Entity: risk:RISK-005
  Details: Non-conformité RGPD (score: 12)
  ✅ Success
```

## 🎯 Prochaines Étapes

Félicitations ! Vous avez créé votre premier projet ISO 27001 en 30 minutes. 🎉

### Pour aller plus loin :

1. **Compléter les risques** :
   ```bash
   iso27001 risk add
   ```
   Ajoutez 10-20 risques supplémentaires pour couvrir tous les aspects de votre organisation.

2. **Implémenter plus de contrôles** :
   ```bash
   iso27001 control list --status not_started
   ```
   Priorisez les contrôles selon vos risques et implémentez-les progressivement.

3. **Générer des politiques** :
   ```bash
   iso27001 policy generate security
   iso27001 policy generate access-control
   iso27001 policy generate incident-response
   ```
   Créez les politiques de sécurité nécessaires.

4. **Exporter pour audit** :
   ```bash
   iso27001 export --format markdown --output audit_package/
   ```
   Préparez un package complet pour votre auditeur externe.

5. **Planifier les revues** :
   - Revue mensuelle des risques
   - Revue trimestrielle des contrôles
   - Audit interne semestriel
   - Audit de certification annuel

## 📚 Ressources Complémentaires

- [Documentation complète](../README.md)
- [Architecture du projet](../../ARCHITECTURE.md)
- [Guide de sécurité](../../SECURITY.md)
- [Norme ISO 27001:2022 officielle](https://www.iso.org/standard/27001)

## 💡 Conseils Pro

1. **Utilisez `iso27001 doctor` régulièrement** pour vérifier la santé de votre projet
2. **Committez vos changements** si vous utilisez Git pour le versioning
3. **Documentez vos décisions** dans les notes des contrôles et risques
4. **Impliquez toute l'équipe** : la sécurité est l'affaire de tous
5. **Automatisez les backups** du répertoire `.iso27001/`

## ❓ Besoin d'Aide ?

- 🐛 Problème technique ? → [GitHub Issues](https://github.com/GitCroque/iso27001-toolbox/issues)
- 💬 Question ? → Consultez la documentation ou ouvrez une discussion
- 🔒 Vulnérabilité ? → Voir [SECURITY.md](../../SECURITY.md)

---

**Bon courage pour votre certification ISO 27001 ! 🚀🔒**
