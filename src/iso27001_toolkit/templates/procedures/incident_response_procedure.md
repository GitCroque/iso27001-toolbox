# Procédure de Réponse aux Incidents de Sécurité

**Organisation:** {{ organization_name }}
**Version:** 1.0
**Date:** {{ effective_date }}

## 1. Objectif
Définir les étapes de réponse à un incident de sécurité.

## 2. Définitions

**Événement** : Occurrence dans un système ou service
**Incident** : Événement compromettant la sécurité de l'information

## 3. Classification

### 3.1 Niveau 1 - Critique
- Violation massive de données
- Ransomware actif
- Compromission systèmes critiques
- **Action** : Immédiate (< 1h)

### 3.2 Niveau 2 - Élevé
- Compromission comptes privilégiés
- Malware actif
- Déni de service
- **Action** : Rapide (< 4h)

### 3.3 Niveau 3 - Moyen
- Tentative intrusion bloquée
- Phishing ciblé
- **Action** : Normale (< 24h)

### 3.4 Niveau 4 - Faible
- Spam
- Violation mineure
- **Action** : Standard (< 72h)

## 4. Processus de réponse

### Phase 1 : Détection et Signalement (0-15 min)

**Qui** : Toute personne détectant l'incident

**Actions** :
1. Noter l'heure de découverte
2. NE PAS éteindre les systèmes
3. NE PAS modifier les données
4. Signaler immédiatement :
   - Email : {{ ciso_email }}
   - Tél : [Hotline sécurité 24/7]
   - Portail : [URL]

**Informations à fournir** :
- Date/heure découverte
- Description incident
- Systèmes affectés
- Actions déjà prises
- Contact

### Phase 2 : Triage et Classification (15-30 min)

**Qui** : RSSI ou délégué

**Actions** :
1. Évaluation initiale
2. Classification niveau 1-4
3. Activation CSIRT si besoin
4. Création ticket incident
5. Notification parties prenantes

**Décision** :
- Niveau 1-2 : Activation CSIRT complète
- Niveau 3-4 : CSIRT réduite

### Phase 3 : Confinement (Immédiat)

**Qui** : CSIRT

**Confinement court terme (< 2h)** :
1. Isoler systèmes affectés
   - Déconnexion réseau si nécessaire
   - Désactivation comptes compromis
2. Préserver les preuves
   - Captures mémoire
   - Logs système
   - Snapshots disques
3. Bloquer la propagation
   - Blocage IP/domaines
   - Désactivation services
   - Mise en quarantaine

**Confinement long terme** :
1. Analyse approfondie
2. Confinement permanent
3. Mise à jour contrôles

### Phase 4 : Éradication (Selon urgence)

**Qui** : CSIRT + IT

**Actions** :
1. Identification cause racine
   - Analyse logs
   - Forensique si nécessaire
   - Investigation approfondie
2. Suppression menace
   - Suppression malware
   - Fermeture backdoors
   - Correction vulnérabilités
3. Renforcement
   - Mise à jour systèmes
   - Correctifs sécurité
   - Amélioration contrôles

### Phase 5 : Récupération (Planifié)

**Qui** : IT + CSIRT + Métier

**Actions** :
1. Plan de récupération
   - Priorisation systèmes
   - Tests en environnement isolé
   - Validation métier
2. Restauration progressive
   - Systèmes critiques d'abord
   - Vérification sécurité
   - Surveillance accrue
3. Retour à la normale
   - Validation fonctionnelle
   - Monitoring renforcé
   - Communication fin incident

### Phase 6 : Post-Incident (< 7 jours)

**Qui** : CSIRT + Direction

**Actions** :
1. Rapport post-incident
   - Chronologie complète
   - Actions entreprises
   - Impact évalué
   - Coûts estimés
2. Leçons apprises
   - Réunion post-mortem
   - Analyse ce qui a marché/échoué
   - Recommandations
3. Amélioration
   - Mise à jour procédures
   - Formation si nécessaire
   - Renforcement contrôles
4. Suivi actions
   - Plan d'action
   - Responsables
   - Échéances
   - Tracking

## 5. CSIRT (Computer Security Incident Response Team)

### 5.1 Composition
- **Lead** : {{ ciso_name }} (RSSI)
- **Membres** :
  - Responsable IT
  - Admin systèmes/réseaux
  - Responsable légal
  - Responsable communication
  - DPO (si données personnelles)
  - Métier (selon incident)

### 5.2 Contacts d'urgence
- RSSI : {{ ciso_email }} / [Tél]
- Hotline : [Numéro 24/7]
- Backup RSSI : [Contact]

## 6. Communication

### 6.1 Interne
**Immédiat** :
- Direction (niveaux 1-2)
- Équipes IT
- Équipes affectées

**Après stabilisation** :
- Communication générale si impact large
- FAQ pour support

### 6.2 Externe

**Obligatoire** :
- **CNIL** : Violation données personnelles (< 72h)
- **ANSSI** : Incidents significatifs
- **Police** : Si cybercriminalité

**Selon contrats** :
- Clients affectés
- Partenaires
- Assurances

**Médias** :
- Uniquement via porte-parole désigné
- Messages approuvés par Direction + Légal
- Coordonner avec communication externe

### 6.3 Restrictions
- Confidentialité stricte
- Pas de déclaration non autorisée
- Messages cohérents

## 7. Préservation des preuves

### 7.1 Collecte
**Ordre de volatilité (du plus au moins)** :
1. Mémoire vive (RAM)
2. État réseau
3. Processus en cours
4. Disques
5. Logs système
6. Sauveg ardes

**Méthodes** :
- Outils forensiques (dd, FTK Imager)
- Captures réseau (tcpdump, Wireshark)
- Snapshots VM
- Photos d'écrans

### 7.2 Chaîne de conservation
- Date/heure collecte
- Qui a collecté
- Hash des preuves (MD5, SHA-256)
- Stockage sécurisé
- Accès restreint et tracé
- Documentation complète

### 7.3 Juridique
- Respect procédures légales
- Possibilité d'utilisation en justice
- Consultation juridique si besoin

## 8. Checklist réponse rapide

### Malware/Ransomware
- [ ] Isoler machine du réseau
- [ ] NE PAS éteindre
- [ ] Capture mémoire si possible
- [ ] Noter processus actifs
- [ ] Identifier fichiers chiffrés
- [ ] Vérifier sauvegardes propres
- [ ] NE PAS payer rançon sans avis

### Compromission compte
- [ ] Désactiver compte immédiatement
- [ ] Révoquer sessions actives
- [ ] Réinitialiser mot de passe
- [ ] Vérifier logs accès
- [ ] Notifier utilisateur
- [ ] Activer MFA si pas fait

### Phishing
- [ ] Ne pas cliquer liens
- [ ] Ne pas ouvrir pièces jointes
- [ ] Transférer email à sécurité
- [ ] Signaler à autres utilisateurs
- [ ] Bloquer expéditeur
- [ ] Vérifier si credentials saisis

### Fuite de données
- [ ] Identifier données exposées
- [ ] Contenir la fuite
- [ ] Évaluer impact
- [ ] Notifier CNIL si < 72h (RGPD)
- [ ] Notifier personnes affectées
- [ ] Documentation complète

## 9. Outils

- **SIEM** : Détection et analyse
- **EDR** : Détection endpoints
- **Forensics** : FTK, EnCase, Autopsy
- **Network** : Wireshark, tcpdump
- **Malware** : VirusTotal, Hybrid Analysis

## 10. Métriques

- Temps moyen de détection (MTTD)
- Temps moyen de réponse (MTTR)
- Nombre incidents par type
- Coût moyen par incident
- Efficacité confinement

## 11. Amélioration continue

Après chaque incident :
- Rapport post-mortem
- Leçons apprises documentées
- Procédures mises à jour
- Formation ciblée
- Tests/simulations

## 12. Exercices

- **Tabletop** : Trimestriel
- **Simulation technique** : Semestriel
- **Test complet** : Annuel

## 13. Contact urgence

**Hotline sécurité 24/7** : [Numéro]
**Email** : {{ ciso_email }}
**RSSI** : {{ ciso_name }}

---
*Réf : Politique de Gestion des Incidents*
