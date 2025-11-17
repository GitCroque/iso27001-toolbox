# Politique de Contrôle d'Accès

**Organisation:** {{ organization_name }}
**Date d'effet:** {{ effective_date }}
**Version:** 1.0
**Propriétaire:** {{ ciso_name }}

## 1. Objectif

Cette politique définit les règles et procédures pour le contrôle d'accès aux systèmes d'information et aux données de {{ organization_name }}.

## 2. Portée

Cette politique s'applique à :
- Tous les utilisateurs (employés, contractuels, tiers)
- Tous les systèmes et applications
- Tous les types d'accès (physique et logique)
- Tous les sites de {{ organization_name }}

## 3. Principes généraux

### 3.1 Principe du moindre privilège
Les utilisateurs reçoivent uniquement les droits d'accès nécessaires à leurs fonctions.

### 3.2 Séparation des tâches
Les fonctions critiques sont divisées entre plusieurs personnes pour prévenir la fraude.

### 3.3 Besoin d'en connaître
L'accès à l'information est limité aux personnes ayant un besoin légitime.

## 4. Gestion des identités

### 4.1 Création des comptes
- Les comptes sont créés sur demande formelle approuvée
- Chaque utilisateur a un identifiant unique et personnel
- Les comptes partagés sont interdits sauf exception justifiée

### 4.2 Cycle de vie des comptes
- **Création** : Dans les 24h suivant l'approbation
- **Modification** : Lors de changement de poste ou de responsabilités
- **Désactivation** : Immédiatement en cas de départ ou suspension
- **Suppression** : 90 jours après désactivation

### 4.3 Revue des comptes
- Revue trimestrielle de tous les comptes actifs
- Revue mensuelle des comptes à privilèges
- Désactivation automatique après 90 jours d'inactivité

## 5. Authentification

### 5.1 Mots de passe

**Exigences minimales :**
- Longueur minimale : 12 caractères
- Complexité : majuscules, minuscules, chiffres et caractères spéciaux
- Historique : les 10 derniers mots de passe ne peuvent être réutilisés
- Expiration : tous les 90 jours
- Verrouillage : après 5 tentatives échouées

**Interdictions :**
- Partage de mots de passe
- Utilisation de mots du dictionnaire
- Informations personnelles (nom, date de naissance, etc.)
- Stockage en clair

### 5.2 Authentification multi-facteurs (MFA)

**Obligatoire pour :**
- Accès administrateurs
- Accès VPN
- Accès aux données confidentielles
- Accès distant

## 6. Autorisation et droits d'accès

### 6.1 Attribution des droits
- Basée sur les rôles et responsabilités
- Approuvée par le responsable hiérarchique
- Documentée et traçable
- Limitée dans le temps si nécessaire

### 6.2 Droits privilégiés
- Attribution restrictive
- Justification documentée
- Revue mensuelle
- Surveillance accrue des activités

### 6.3 Accès distant
- VPN avec MFA obligatoire
- Équipement conforme aux standards de sécurité
- Interdiction d'accès depuis des réseaux publics non sécurisés

## 7. Contrôles d'accès logiques

### 7.1 Systèmes d'exploitation
- Comptes utilisateurs nominatifs
- Séparation des comptes administrateurs et utilisateurs
- Journalisation des activités privilégiées

### 7.2 Applications
- Contrôle d'accès basé sur les rôles (RBAC)
- Session timeout après 15 minutes d'inactivité
- Déconnexion automatique en fin de journée

### 7.3 Bases de données
- Accès direct limité aux DBA
- Authentification forte
- Chiffrement des données sensibles

### 7.4 Réseaux
- Segmentation réseau
- Pare-feu avec règles restrictives
- VLANs pour séparer les environnements

## 8. Contrôles d'accès physiques

### 8.1 Zones de sécurité
- **Zone publique** : Accès libre
- **Zone restreinte** : Badge requis
- **Zone hautement restreinte** : Badge + autorisation spéciale

### 8.2 Badges d'accès
- Badges personnels et non transférables
- Restitution immédiate en cas de départ
- Désactivation en cas de perte

### 8.3 Visiteurs
- Enregistrement obligatoire
- Badge visiteur
- Accompagnement permanent dans les zones restreintes

## 9. Accès tiers et fournisseurs

- Accords de confidentialité signés
- Accès limité au strict nécessaire
- Surveillance des activités
- Révocation immédiate en fin de contrat

## 10. Surveillance et audit

### 10.1 Journalisation
- Tous les accès sont journalisés
- Conservation des logs : 12 mois minimum
- Revue régulière des logs d'accès privilégiés

### 10.2 Alertes
- Tentatives d'accès échouées répétées
- Accès en dehors des heures normales
- Activités suspectes

## 11. Responsabilités

### 11.1 RSSI
- Définir et maintenir la politique
- Superviser l'implémentation
- Auditer la conformité

### 11.2 Administrateurs systèmes
- Implémenter les contrôles techniques
- Gérer les comptes et droits
- Surveiller les accès

### 11.3 Responsables hiérarchiques
- Approuver les demandes d'accès
- Signaler les changements (départs, mutations)
- Revoir régulièrement les droits de leur équipe

### 11.4 Utilisateurs
- Protéger leurs identifiants
- Signaler toute anomalie
- Se déconnecter après utilisation

## 12. Exceptions

Toute exception à cette politique doit être :
- Justifiée par écrit
- Approuvée par le RSSI
- Limitée dans le temps
- Documentée et révisée régulièrement

## 13. Non-conformité

Le non-respect de cette politique peut entraîner :
- Révocation des droits d'accès
- Sanctions disciplinaires
- Poursuites légales

## 14. Révision

Cette politique est révisée annuellement ou en cas de changement significatif.

## 15. Références

- Politique de sécurité de l'information
- Procédure de gestion des comptes
- Procédure de gestion des incidents

## 16. Approbation

**Approuvé par :** [Nom du Directeur Général]
**Titre :** Directeur Général
**Date :** {{ effective_date }}
**Signature :** _________________________

## 17. Contact

**RSSI :** {{ ciso_name }}
**Email :** {{ ciso_email }}

---

*Document généré le {{ current_date }}*
*Conforme à ISO/IEC 27001:2022 - Contrôles A.5.15, A.5.16, A.5.17, A.5.18*
