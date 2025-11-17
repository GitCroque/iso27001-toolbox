# Politique de Gestion des Fournisseurs

**Organisation:** {{ organization_name }}
**Date d'effet:** {{ effective_date }}
**Version:** 1.0

## 1. Objectif
Assurer la protection des actifs accessibles par les fournisseurs et maintenir un niveau approprié de sécurité.

## 2. Évaluation des fournisseurs

### 2.1 Avant engagement
- Évaluation sécurité selon criticité
- Vérification références
- Audits si nécessaire
- Revue certifications (ISO 27001, etc.)

### 2.2 Classification
- **Critique** : Accès données sensibles ou systèmes critiques
- **Important** : Accès données internes
- **Standard** : Accès limité

## 3. Contrats et accords

### 3.1 Clauses obligatoires
- Confidentialité et non-divulgation
- Exigences de sécurité
- Droit d'audit
- Notification d'incidents sous 24h
- Responsabilités et pénalités
- Sous-traitance interdite sans accord

### 3.2 Annexe sécurité
Pour fournisseurs critiques :
- Contrôles de sécurité requis
- Gestion des accès
- Retour/destruction des données
- Conformité réglementaire

## 4. Gestion des accès fournisseurs

- Principe du moindre privilège
- Comptes nominatifs (pas de partage)
- MFA obligatoire
- Durée limitée dans le temps
- Révocation immédiate fin contrat
- Journalisation activités

## 5. Services Cloud

### 5.1 Avant adoption
- Évaluation sécurité du fournisseur
- Localisation des données
- Certifications (ISO 27001, SOC 2)
- SLA et disponibilité
- Procédure de sortie

### 5.2 Utilisation
- Shadow IT interdit
- Validation RSSI obligatoire
- Chiffrement données sensibles
- Revue annuelle

## 6. Surveillance et revue

### 6.1 Fournisseurs critiques
- Revue trimestrielle performance sécurité
- Audits annuels si contractuels
- Surveillance incidents

### 6.2 Tous fournisseurs
- Revue annuelle des accords
- Mise à jour exigences sécurité
- Vérification conformité

## 7. Incidents impliquant fournisseurs

- Notification obligatoire sous 24h
- Coopération investigation
- Mise en œuvre actions correctives
- Rapport post-incident

## 8. Fin de relation

- Restitution tous actifs {{ organization_name }}
- Suppression/destruction données
- Révocation tous accès
- Confirmation écrite destruction
- Rappel obligations confidentialité continues

## 9. Responsabilités

**Achats :** Sélection fournisseurs
**Juridique :** Revue contrats
**RSSI :** Validation sécurité, audits
**Métiers :** Suivi performance

## 10. Contact
**RSSI :** {{ ciso_name }} - {{ ciso_email }}

---
*Conforme ISO 27001:2022 - Contrôles A.5.19-23*
