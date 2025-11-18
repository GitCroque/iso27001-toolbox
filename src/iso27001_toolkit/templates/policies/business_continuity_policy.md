# Politique de Continuité d'Activité

**Organisation:** {{ organization_name }}
**Date d'effet:** {{ effective_date }}
**Version:** 1.0
**Propriétaire:** {{ ciso_name }}

## 1. Objectif

Établir un cadre pour assurer la continuité des opérations critiques de {{ organization_name }} en cas de perturbation majeure.

## 2. Portée

Cette politique couvre tous les processus critiques, systèmes et ressources nécessaires aux opérations de {{ organization_name }}.

## 3. Objectifs de continuité

- **RTO (Recovery Time Objective)** : Temps maximal d'interruption acceptable
- **RPO (Recovery Point Objective)** : Perte de données maximale acceptable
- **MTPD (Maximum Tolerable Period of Disruption)** : Période maximale tolérable

## 4. Analyse d'impact (BIA)

### 4.1 Processus critiques identifiés
- Liste maintenue et revue annuellement
- Classification par criticité
- Identification des dépendances
- Ressources nécessaires documentées

### 4.2 Niveaux de criticité
| Niveau | RTO | RPO | Exemple |
|--------|-----|-----|---------|
| Critique | < 4h | < 1h | Production, Facturation |
| Important | < 24h | < 4h | Support client |
| Moyen | < 72h | < 24h | Reporting |
| Faible | > 72h | > 24h | Archives |

## 5. Stratégies de continuité

### 5.1 Infrastructure IT
- Site de secours ou cloud
- Redondance des systèmes critiques
- Sauvegardes régulières et testées
- Capacité de basculement

### 5.2 Ressources humaines
- Équipes de secours identifiées
- Compétences croisées
- Télétravail possible
- Personnel essentiel désigné

### 5.3 Installations
- Site alternatif identifié
- Accords avec fournisseurs
- Équipements de secours

## 6. Plan de Continuité d'Activité (PCA)

### 6.1 Contenu du PCA
- Procédures d'activation
- Contacts d'urgence
- Procédures de reprise
- Ressources nécessaires
- Communications

### 6.2 Activation du PCA
Déclenchement par :
- Direction générale
- {{ ciso_name }} (RSSI)
- Responsable de la continuité

## 7. Plan de Reprise d'Activité IT (PRA)

### 7.1 Procédures de sauvegarde
- Quotidienne : Données critiques
- Hebdomadaire : Systèmes complets
- Mensuelle : Archives
- Stockage hors site des sauvegardes

### 7.2 Procédures de restauration
- Ordre de priorité des systèmes
- Procédures détaillées
- Vérification de l'intégrité
- Tests de restauration mensuels

## 8. Communication de crise

### 8.1 Cellule de crise
- Direction
- RSSI : {{ ciso_name }}
- Responsables opérationnels
- Communication
- Juridique

### 8.2 Communications
- **Interne** : Personnel informé rapidement
- **Clients** : Information appropriée
- **Fournisseurs** : Coordination
- **Médias** : Porte-parole unique

## 9. Tests et exercices

### 9.1 Fréquence
- **Tests techniques** : Mensuels (sauvegardes)
- **Exercices de simulation** : Trimestriels
- **Exercice grandeur nature** : Annuel
- **Revue du plan** : Semestrielle

### 9.2 Documentation
- Rapport de chaque test
- Leçons apprises
- Actions correctives
- Mise à jour des procédures

## 10. Formation

- Formation initiale pour équipes de crise
- Rafraîchissement annuel
- Nouveaux arrivants dans les 30 jours
- Sensibilisation générale du personnel

## 11. Responsabilités

**Direction :**
- Approuver le PCA/PRA
- Allouer les ressources
- Déclencher l'activation

**RSSI :**
- Maintenir le PCA/PRA
- Coordonner les tests
- Gérer la crise IT

**Responsables de processus :**
- Identifier les besoins de continuité
- Maintenir les procédures
- Participer aux tests

## 12. Revue et amélioration

- Revue annuelle obligatoire
- Mise à jour après incidents
- Amélioration continue
- Benchmark des meilleures pratiques

## 13. Approbation

**Approuvé par :** [Nom du Directeur Général]
**Titre :** Directeur Général
**Date :** {{ effective_date }}

## 14. Contact

**RSSI :** {{ ciso_name }}
**Email :** {{ ciso_email }}
**Urgence :** [Numéro 24/7]

---

*Conforme à ISO/IEC 27001:2022 - Contrôles A.5.29, A.5.30*
