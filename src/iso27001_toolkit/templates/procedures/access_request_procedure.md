# Procédure de Demande d'Accès

**Organisation:** {{ organization_name }}
**Version:** 1.0
**Date:** {{ effective_date }}

## 1. Objectif
Définir le processus de demande, approbation et provisionnement des accès aux systèmes.

## 2. Portée
Tous les accès aux systèmes d'information de {{ organization_name }}.

## 3. Processus

### 3.1 Demande d'accès (Demandeur)

1. Remplir le formulaire de demande d'accès
2. Spécifier :
   - Systèmes/applications nécessaires
   - Niveau d'accès requis
   - Justification métier
   - Durée (permanent/temporaire)
3. Soumettre à son manager

### 3.2 Approbation (Manager)

1. Vérifier la justification
2. Confirmer le besoin métier
3. Valider le niveau d'accès (principe du moindre privilège)
4. Approuver ou rejeter avec commentaires
5. Transmettre à l'équipe IT

### 3.3 Validation sécurité (RSSI)

Pour les accès privilégiés uniquement :
1. Revue de la demande
2. Vérification conformité politique
3. Approbation finale
4. Transmission IT

### 3.4 Provisionnement (IT)

1. Vérifier les approbations
2. Créer le compte
3. Attribuer les droits
4. Configurer MFA si nécessaire
5. Notifier l'utilisateur
6. Documenter dans l'inventaire

### 3.5 Confirmation (Utilisateur)

1. Recevoir notification
2. Première connexion
3. Changement mot de passe temporaire
4. Configuration MFA
5. Accuser réception

## 4. Délais SLA

| Type d'accès | Délai maximum |
|--------------|---------------|
| Standard | 2 jours ouvrés |
| Privilégié | 5 jours ouvrés |
| Urgence (validée) | 4 heures |
| Temporaire | 1 jour ouvré |

## 5. Accès temporaires

- Durée maximale : 90 jours
- Revue à mi-parcours
- Révocation automatique à l'échéance
- Possibilité de renouvellement (nouvelle demande)

## 6. Modification d'accès

- Même processus que création
- Indiquer les changements souhaités
- Approbation manager requise

## 7. Révocation d'accès

### 7.1 Départ d'un employé
- RH notifie IT immédiatement
- Désactivation le dernier jour
- Suppression après 90 jours

### 7.2 Changement de poste
- Manager notifie IT
- Revue des accès existants
- Ajustement selon nouveau rôle

### 7.3 Suspicion sécurité
- RSSI peut révoquer immédiatement
- Investigation parallèle
- Réactivation si justifiée

## 8. Revue des accès

- Trimestrielle pour tous les utilisateurs
- Mensuelle pour comptes privilégiés
- Manager confirme ou demande révocation
- Rapport au RSSI

## 9. Documentation

Chaque accès documenté avec :
- Identifiant utilisateur
- Systèmes/applications
- Niveau d'accès
- Date création
- Approbateurs
- Date dernière revue

## 10. Formulaire requis
Voir : `formulaire_demande_acces.md`

## 11. Contact
**IT Support :** [Email/Tel]
**RSSI :** {{ ciso_email }}

---
*Réf: Politique de Contrôle d'Accès*
