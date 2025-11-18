# Politique de Gestion des Incidents de Sécurité

**Organisation:** {{ organization_name }}
**Date d'effet:** {{ effective_date }}
**Version:** 1.0
**Propriétaire:** {{ ciso_name }}

## 1. Objectif

Cette politique établit le cadre pour la détection, le signalement, l'évaluation et la réponse aux incidents de sécurité de l'information chez {{ organization_name }}.

## 2. Portée

Cette politique couvre tous les incidents de sécurité affectant :
- Les systèmes d'information
- Les réseaux
- Les données
- Le personnel
- Les installations physiques

## 3. Définitions

**Événement de sécurité** : Occurrence identifiée d'un état système, service ou réseau indiquant une possible violation de politique ou un échec de contrôle.

**Incident de sécurité** : Événement ou série d'événements compromettant la confidentialité, l'intégrité ou la disponibilité de l'information.

**Violation de données** : Incident entraînant la divulgation non autorisée de données personnelles ou sensibles.

## 4. Classification des incidents

### 4.1 Niveau 1 - Critique
- Violation de données personnelles à grande échelle
- Compromission de systèmes critiques
- Ransomware affectant les opérations
- Impact financier > 100 000€

**Temps de réponse :** Immédiat (< 1 heure)

### 4.2 Niveau 2 - Élevé
- Compromission de comptes privilégiés
- Malware détecté sur plusieurs systèmes
- Défacement de site web
- Déni de service impactant les opérations

**Temps de réponse :** < 4 heures

### 4.3 Niveau 3 - Moyen
- Tentatives d'intrusion bloquées
- Phishing ciblé
- Perte d'équipement contenant des données
- Violation mineure de politique

**Temps de réponse :** < 24 heures

### 4.4 Niveau 4 - Faible
- Spam
- Tentatives d'accès non autorisé isolées
- Violations mineures de procédure

**Temps de réponse :** < 72 heures

## 5. Signalement des incidents

### 5.1 Qui doit signaler
Tout employé, contractuel ou tiers ayant connaissance d'un incident réel ou suspecté.

### 5.2 Comment signaler

**Canaux de signalement :**
- Email : {{ ciso_email }}
- Téléphone : [Numéro hotline sécurité]
- Portail interne : [URL portail incidents]

**Informations à fournir :**
- Date et heure de découverte
- Description de l'incident
- Systèmes ou données affectés
- Actions déjà entreprises
- Contact du signalant

### 5.3 Délais de signalement
- **Incidents critiques** : Immédiatement
- **Autres incidents** : Dans les 24 heures

## 6. Équipe de réponse aux incidents (CSIRT)

### 6.1 Composition
- **Chef d'équipe :** {{ ciso_name }} (RSSI)
- **Membres :**
  - Responsable IT
  - Responsable Sécurité Réseau
  - Responsable Légal
  - Responsable Communication
  - DPO : {{ dpo_name }}

### 6.2 Responsabilités
- Évaluer et classifier les incidents
- Coordonner la réponse
- Documenter les actions
- Communiquer avec les parties prenantes
- Conduire l'analyse post-incident

## 7. Processus de gestion des incidents

### 7.1 Phase 1 : Détection et signalement
1. Détection de l'incident (automatique ou manuelle)
2. Signalement au CSIRT
3. Enregistrement dans le système de tickets

### 7.2 Phase 2 : Évaluation et classification
1. Analyse initiale
2. Classification du niveau de sévérité
3. Activation du CSIRT approprié
4. Notification des parties prenantes

### 7.3 Phase 3 : Confinement
1. Isolation des systèmes affectés
2. Préservation des preuves
3. Blocage de la menace
4. Limitation de la propagation

### 7.4 Phase 4 : Éradication
1. Identification de la cause racine
2. Suppression de la menace
3. Correction des vulnérabilités
4. Renforcement des contrôles

### 7.5 Phase 5 : Récupération
1. Restauration des systèmes
2. Validation du fonctionnement
3. Surveillance accrue
4. Retour à la normale

### 7.6 Phase 6 : Leçons apprises
1. Analyse post-incident
2. Documentation des leçons apprises
3. Mise à jour des procédures
4. Formation du personnel
5. Amélioration des contrôles

## 8. Préservation des preuves

### 8.1 Collecte
- Journaux système
- Captures réseau
- Images disques
- Captures d'écran
- Emails

### 8.2 Chaîne de conservation
- Documentation de la collecte
- Stockage sécurisé
- Contrôle d'accès strict
- Traçabilité complète

## 9. Communication

### 9.1 Communication interne
- Direction : Incidents critiques et élevés
- Équipes IT : Selon besoin
- Personnel affecté : Information appropriée
- Tous : Incidents majeurs via communication officielle

### 9.2 Communication externe

**Autorités de régulation :**
- CNIL : Violations de données personnelles (< 72h)
- ANSSI : Incidents significatifs
- Police/Gendarmerie : Incidents criminels

**Clients :**
- Si leurs données sont affectées
- Communication coordonnée par Direction + Legal

**Médias :**
- Uniquement via le Responsable Communication
- Après approbation de la Direction

### 9.3 Restrictions
- Aucune communication non autorisée
- Confidentialité stricte
- Messages cohérents et approuvés

## 10. Documentation

Chaque incident doit être documenté avec :
- **ID incident** : Identifiant unique
- **Classification** : Niveau et type
- **Chronologie** : Timeline complète
- **Actions entreprises** : Détails de la réponse
- **Impact** : Systèmes, données, utilisateurs affectés
- **Coûts** : Estimation des coûts directs et indirects
- **Leçons apprises** : Analyse et recommandations

## 11. Métriques et reporting

### 11.1 Métriques clés
- Nombre d'incidents par catégorie
- Temps moyen de détection
- Temps moyen de réponse
- Temps moyen de résolution
- Coût moyen par incident

### 11.2 Reporting
- **Mensuel** : Dashboard incidents au RSSI
- **Trimestriel** : Rapport à la Direction
- **Annuel** : Revue complète et tendances

## 12. Tests et exercices

- **Exercices de table** : Trimestriels
- **Simulations techniques** : Semestriels
- **Tests de restauration** : Mensuels
- **Revue du plan** : Annuelle

## 13. Formation

- Formation initiale obligatoire pour tous les employés
- Formation approfondie pour le CSIRT
- Rappels trimestriels
- Mise à jour lors de changements majeurs

## 14. Responsabilités

### 14.1 Tous les employés
- Signaler immédiatement tout incident suspecté
- Ne pas tenter de résoudre seul un incident de sécurité
- Coopérer avec le CSIRT

### 14.2 RSSI
- Maintenir et améliorer le processus
- Diriger le CSIRT
- Coordonner la réponse
- Rapporter à la Direction

### 14.3 Direction
- Allouer les ressources nécessaires
- Soutenir les décisions du CSIRT
- Approuver les communications externes

## 15. Amélioration continue

Le processus de gestion des incidents est amélioré par :
- Analyse des incidents passés
- Retours d'expérience
- Veille sur les menaces
- Benchmark avec les meilleures pratiques

## 16. Révision

Cette politique est révisée :
- Annuellement
- Après tout incident majeur
- Lors de changements organisationnels significatifs

## 17. Références

- Politique de sécurité de l'information
- Plan de continuité d'activité
- Procédure de sauvegarde et restauration
- Politique de communication de crise

## 18. Approbation

**Approuvé par :** [Nom du Directeur Général]
**Titre :** Directeur Général
**Date :** {{ effective_date }}
**Signature :** _________________________

## 19. Contact

**CSIRT Lead :** {{ ciso_name }}
**Email :** {{ ciso_email }}
**Hotline :** [Numéro d'urgence 24/7]

---

*Document généré le {{ current_date }}*
*Conforme à ISO/IEC 27001:2022 - Contrôles A.5.24, A.5.25, A.5.26, A.5.27, A.5.28*
