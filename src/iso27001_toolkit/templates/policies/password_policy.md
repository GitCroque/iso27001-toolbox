# Politique de Gestion des Mots de Passe

**Organisation:** {{ organization_name }}
**Date d'effet:** {{ effective_date }}
**Version:** 1.0

## 1. Objectif
Établir les exigences pour la création, l'utilisation et la gestion des mots de passe.

## 2. Exigences des mots de passe

### 2.1 Longueur et complexité

**Comptes utilisateurs standard :**
- Minimum 12 caractères
- Au moins une majuscule
- Au moins une minuscule
- Au moins un chiffre
- Au moins un caractère spécial (@, #, $, %, etc.)

**Comptes privilégiés/administrateurs :**
- Minimum 16 caractères
- Même complexité que standard
- Changement plus fréquent

**Comptes de service/applications :**
- Minimum 24 caractères
- Complexité maximale
- Génération aléatoire obligatoire

### 2.2 Exemples

✅ **Bons mots de passe :**
- `J'aim3L3s!Croissants2024`
- `P@riS#T0ur_Eiff3l!`
- `Caf3-Au-Lait$Matin`

❌ **Mauvais mots de passe :**
- `Password123` - Trop simple
- `123456` - Trop court
- `azerty` - Commun
- `{{ organization_name }}2024` - Prévisible

## 3. Interdictions

### 3.1 Absolument interdit
- Mots du dictionnaire
- Noms propres (personnes, lieux)
- Dates (naissance, anniversaire)
- Informations personnelles
- Séquences clavier (azerty, qwerty)
- Mots de passe précédents
- Mots de passe communs (Password, Admin, etc.)
- Informations de l'organisation

### 3.2 Partage
- ❌ Jamais partager son mot de passe
- ❌ Jamais communiquer par email/SMS
- ❌ Jamais écrire sur papier non sécurisé
- ❌ Jamais le dire à voix haute
- ❌ Jamais utiliser le même sur plusieurs systèmes

## 4. Changement de mots de passe

### 4.1 Fréquence

| Type de compte | Fréquence |
|----------------|-----------|
| Utilisateur standard | 90 jours |
| Compte privilégié | 60 jours |
| Compte administrateur | 45 jours |
| Compte de service | 180 jours ou lors rotation |

### 4.2 Circonstances spéciales
Changement immédiat si :
- Suspicion de compromission
- Après incident de sécurité
- Employé ayant connu le mot de passe a quitté
- Demande du RSSI
- Après support technique

### 4.3 Historique
- Les 10 derniers mots de passe ne peuvent être réutilisés
- Vérification automatique par le système

## 5. Mot de passe temporaire

### 5.1 Première connexion
- Mot de passe temporaire complexe
- Changement obligatoire à la première connexion
- Validité 24h maximum
- Envoi sécurisé (pas par email)

### 5.2 Réinitialisation
- Vérification identité obligatoire
- Nouveau mot de passe temporaire
- Délai de validité court
- Notification utilisateur

## 6. Stockage des mots de passe

### 6.1 Gestionnaires de mots de passe

**Approuvés :**
- 1Password (Enterprise)
- Bitwarden (Enterprise)
- KeePass (avec politique)
- LastPass (Enterprise)

**Avantages :**
- Génération mots de passe forts
- Stockage chiffré
- Un seul mot de passe maître à retenir
- Remplissage automatique

### 6.2 Interdictions de stockage
- ❌ Fichier texte non chiffré
- ❌ Post-it sur écran
- ❌ Carnet non sécurisé
- ❌ Email
- ❌ Messagerie instantanée
- ❌ Navigateur (sauf si chiffré)
- ❌ Feuille de calcul non chiffrée

### 6.3 Stockage système
- Hachage avec sel (salt)
- Algorithmes approuvés (bcrypt, Argon2)
- Jamais en clair
- Base de données chiffrée

## 7. Authentification multi-facteurs (MFA)

### 7.1 Obligatoire pour
- Accès VPN
- Webmail
- Comptes privilégiés
- Systèmes critiques
- Accès distant

### 7.2 Méthodes approuvées
1. Application d'authentification (Google Authenticator, Microsoft Authenticator)
2. Clé de sécurité matérielle (YubiKey)
3. Codes de secours (à stocker en lieu sûr)
4. SMS (en dernier recours)

### 7.3 Backup codes
- Générer et sauvegarder
- Stocker en lieu physique sûr
- Ne pas stocker numériquement non chiffré

## 8. Verrouillage de compte

### 8.1 Tentatives échouées
- 5 tentatives maximum
- Verrouillage automatique 30 minutes
- Notification utilisateur et sécurité
- Réinitialisation par IT après vérification

### 8.2 Inactivité
- Verrouillage automatique après 5 minutes
- Mot de passe requis pour déverrouillage
- Pas de contournement possible

## 9. Mots de passe par défaut

### 9.1 Équipements réseau
- Changement immédiat après installation
- Mot de passe unique par équipement
- Documentation dans gestionnaire sécurisé

### 9.2 Applications
- Changement lors du premier déploiement
- Pas de comptes par défaut en production
- Désactivation comptes non utilisés

## 10. Passphrase (phrase de passe)

Alternative acceptée :
- Minimum 20 caractères
- 4 mots minimum non liés
- Espaces et caractères spéciaux
- Exemple : `Café-Bleu!Tour&Soleil#Paris`

## 11. Cas particuliers

### 11.1 Comptes partagés
- Éviter autant que possible
- Si nécessaire : autorisation RSSI
- Traçabilité qui utilise quand
- Rotation fréquente

### 11.2 Comptes de service
- Génération aléatoire 32+ caractères
- Stockage dans coffre-fort sécurisé
- Accès restreint
- Rotation planifiée

### 11.3 Certificats et clés
- Mots de passe forts pour clés privées
- Stockage HSM si possible
- Procédure d'escrow documentée

## 12. Récupération compte

### 12.1 Processus
1. Demande via hotline IT
2. Vérification identité (3 questions minimum)
3. Validation par manager si nécessaire
4. Génération mot de passe temporaire
5. Notification utilisateur

### 12.2 Questions secrètes
- Éviter si possible (MFA préféré)
- Si utilisées : réponses non évidentes
- Pas d'informations publiques

## 13. Formation et sensibilisation

### 13.1 Utilisateurs
- Formation initiale obligatoire
- Rappels trimestriels
- Tests (phishing simulé)
- Bonnes pratiques

### 13.2 Sujets
- Création mots de passe forts
- Utilisation gestionnaire
- Reconnaissance phishing
- MFA
- Signalement incidents

## 14. Surveillance

### 14.1 Indicateurs
- Tentatives échouées
- Mots de passe faibles détectés
- Comptes sans MFA
- Mots de passe non changés

### 14.2 Audits
- Scan mots de passe faibles
- Vérification complexité
- Contrôle expirations
- Analyse breaches

## 15. Incidents

### 15.1 À signaler immédiatement
- Mot de passe compromis
- Tentatives accès inhabituelles
- Email de réinitialisation non sollicité
- Comptes verrouillés sans raison

### 15.2 Actions
- Changement immédiat
- Vérification activité suspecte
- Notification RSSI : {{ ciso_email }}
- Investigation si nécessaire

## 16. Exceptions

- Autorisation écrite RSSI requise
- Justification documentée
- Durée limitée
- Compensé par autres contrôles

## 17. Outils techniques

### 17.1 Validation
- Vérification complexité en temps réel
- Comparaison bases de données breaches
- Détection mots de passe faibles

### 17.2 Gestion
- Réinitialisation self-service
- Notifications expiration
- Portail de gestion

## 18. Conformité

- Audit annuel
- Revue politique
- Tests de pénétration
- Conformité RGPD

## 19. Contact
**RSSI :** {{ ciso_name }} - {{ ciso_email }}
**Hotline IT :** [Numéro]

---
*Conforme ISO 27001:2022 - Contrôles A.5.17, A.8.5*
