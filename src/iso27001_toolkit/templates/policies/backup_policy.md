# Politique de Sauvegarde et Restauration

**Organisation:** {{ organization_name }}
**Date d'effet:** {{ effective_date }}
**Version:** 1.0

## 1. Objectif
Garantir la disponibilité et la récupérabilité des données critiques de {{ organization_name }}.

## 2. Portée
Toutes les données et systèmes critiques de l'organisation.

## 3. Classification et stratégie

### 3.1 Données critiques (Tier 1)
- **RPO** : 1 heure maximum
- **RTO** : 4 heures maximum
- **Fréquence** : Continue ou horaire
- **Rétention** : 90 jours
- **Exemples** : Base de données production, transactions

### 3.2 Données importantes (Tier 2)
- **RPO** : 24 heures
- **RTO** : 24 heures
- **Fréquence** : Quotidienne
- **Rétention** : 30 jours
- **Exemples** : Documents partagés, emails

### 3.3 Données standard (Tier 3)
- **RPO** : 7 jours
- **RTO** : 72 heures
- **Fréquence** : Hebdomadaire
- **Rétention** : 30 jours
- **Exemples** : Archives, logs anciens

## 4. Stratégie 3-2-1-1-0

- **3** copies des données
- **2** types de supports différents
- **1** copie hors site
- **1** copie offline (air-gapped)
- **0** erreur de vérification

## 5. Types de sauvegardes

### 5.1 Complète (Full)
- Toutes les données
- **Fréquence** : Hebdomadaire (dimanche)
- Baseline pour restauration

### 5.2 Incrémentielle
- Données modifiées depuis dernière sauvegarde
- **Fréquence** : Quotidienne (lundi-samedi)
- Restauration plus rapide

### 5.3 Différentielle
- Données modifiées depuis dernière complète
- **Fréquence** : Selon besoin
- Compromis temps/espace

### 5.4 Continue (CDP)
- Réplication en temps réel
- Pour systèmes critiques uniquement
- RPO quasi-zéro

## 6. Calendrier type

| Jour | Type | Systèmes |
|------|------|----------|
| Lundi-Samedi | Incrémentielle | Tous |
| Dimanche | Complète | Tous |
| Mensuel (1er) | Complète + Archive | Tous |
| Trimestriel | Complète + Archivage longue durée | Critiques |

## 7. Stockage

### 7.1 Stockage primaire
- Baie de sauvegarde dédiée
- Datacenter principal
- Chiffrement activé
- Accès restreint

### 7.2 Stockage secondaire (hors site)
- Datacenter distant (> 100 km)
- Réplication automatique
- Même niveau de sécurité
- Accessible en cas de sinistre principal

### 7.3 Stockage tertiaire (offline)
- Bandes magnétiques ou disques amovibles
- Coffre-fort ignifuge
- Rotation mensuelle
- Test annuel restauration

### 7.4 Cloud
- Fournisseur cloud certifié (ISO 27001)
- Chiffrement bout-en-bout
- Localisation EU pour RGPD
- Contrat clair sur propriété données

## 8. Chiffrement

### 8.1 En transit
- TLS 1.3 minimum
- VPN pour transferts distants
- Vérification intégrité

### 8.2 Au repos
- AES-256 minimum
- Gestion clés sécurisée
- Clés différentes par site
- Procédure d'escrow des clés

## 9. Vérification et tests

### 9.1 Vérification automatique
- Après chaque sauvegarde
- Checksum/hash
- Notification si échec
- Tentative de retry

### 9.2 Tests de restauration

| Fréquence | Scope | Responsable |
|-----------|-------|-------------|
| Mensuel | Échantillon fichiers | IT |
| Trimestriel | Serveur complet (non-prod) | IT + Métier |
| Semestriel | Système critique complet | IT + Direction |
| Annuel | DR complet | Tous |

### 9.3 Documentation
- Rapport de chaque test
- Temps de restauration mesuré
- Problèmes identifiés
- Actions correctives

## 10. Restauration

### 10.1 Processus
1. Demande formelle (ticket)
2. Validation par manager
3. Évaluation impact
4. Choix point de restauration
5. Restauration (env. test d'abord si possible)
6. Vérification intégrité
7. Validation métier
8. Mise en production si OK

### 10.2 Délais
- **Urgente** : Immédiat
- **Haute** : < 4h
- **Normale** : < 24h
- **Basse** : < 72h

### 10.3 Priorités
1. Systèmes critiques production
2. Base de données
3. Serveurs applicatifs
4. Postes de travail
5. Archives

## 11. Sauvegardes spécifiques

### 11.1 Base de données
- Dump logique quotidien
- Snapshot au niveau stockage
- Logs de transactions
- Point-in-time recovery possible

### 11.2 Machines virtuelles
- Snapshot VM
- Sauvegarde agent inside VM
- Application-aware backup
- Test restauration VM complète

### 11.3 SaaS/Cloud
- Export données régulier
- API de backup si disponible
- Ne pas compter uniquement sur fournisseur
- Vérifier qui est responsable

### 11.4 Postes de travail
- Données utilisateur uniquement
- Stockage réseau/cloud préféré
- Responsabilité utilisateur
- Restauration self-service si possible

### 11.5 Configuration
- Fichiers de configuration
- Scripts d'installation
- Documentation as Code
- Versioning Git

## 12. Rétention

### 12.1 Quotidiennes
- 7 derniers jours
- Rotation automatique

### 12.2 Hebdomadaires
- 4 dernières semaines

### 12.3 Mensuelles
- 12 derniers mois

### 12.4 Annuelles
- 7 ans (conformité légale)
- Archive froide
- Support stable (pas de bandes)

### 12.5 Suppression
- Effacement sécurisé
- Certificat si sensible
- Traçabilité

## 13. Surveillance

### 13.1 Indicateurs (KPI)
- Taux de réussite sauvegardes
- Temps moyen de sauvegarde
- Espace utilisé
- Taux de croissance
- Temps moyen de restauration (MTR)

### 13.2 Alertes
- Échec sauvegarde
- Espace disque < 20%
- Durée anormalement longue
- Vérification échouée

### 13.3 Rapports
- Hebdomadaire : Statut sauvegardes
- Mensuel : KPIs et tendances
- Trimestriel : Tests restauration
- Annuel : Bilan complet

## 14. Responsabilités

### 14.1 Équipe IT
- Configurer et maintenir solution
- Surveiller sauvegardes
- Effectuer restaurations
- Tests réguliers

### 14.2 Propriétaires données
- Identifier données critiques
- Définir RPO/RTO
- Valider restaurations
- Participer aux tests

### 14.3 RSSI
- Vérifier sécurité
- Audit conformité
- Gestion des incidents

## 15. Reprise après sinistre (DR)

### 15.1 Scénarios
- Panne matérielle
- Corruption données
- Ransomware
- Sinistre datacenter
- Erreur humaine

### 15.2 Plan DR
- Procédures détaillées
- Ordre de restauration
- Contacts d'urgence
- Fournisseurs critiques
- Tests annuels

## 16. Ransomware et Malware

### 16.1 Protection
- Sauvegardes immutables
- Air gap (offline)
- MFA sur accès sauvegardes
- Détection ransomware
- Snapshots fréquents

### 16.2 En cas d'attaque
1. Isoler systèmes infectés
2. NE PAS restaurer immédiatement
3. Vérifier sauvegardes non infectées
4. Scanner sauvegardes antivirus
5. Restaurer version propre
6. Investigation forensique

## 17. Conformité

### 17.1 RGPD
- Sauvegarde données personnelles sécurisée
- Respect durées de conservation
- Droit à l'effacement applicable
- Notification breach si sauvegardes impactées

### 17.2 Audit
- Documentation complète
- Logs d'activité
- Preuves de tests
- Conformité politique

## 18. Documentation

- Inventaire des systèmes sauvegardés
- Procédures de sauvegarde
- Procédures de restauration
- Résultats tests
- Configuration systèmes
- Contacts et escalade

## 19. Amélioration continue

- Revue après chaque incident
- Retour des tests
- Évolution besoins métier
- Nouvelles technologies
- Optimisation coûts

## 20. Contact
**RSSI :** {{ ciso_name }} - {{ ciso_email }}
**IT Backup :** [Contact]

---
*Conforme ISO 27001:2022 - Contrôles A.8.13, A.8.14, A.5.29, A.5.30*
