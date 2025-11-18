# Checklist d'Audit ISO 27001:2022

**Organisation:** {{ organization_name }}
**Date d'audit:** {{ audit_date }}
**Auditeur:** {{ auditor_name }}
**Type d'audit:** {{ audit_type }}

## 1. Informations Générales

### 1.1 Périmètre de Certification
{{ certification_scope }}

### 1.2 Sites Concernés
{% if sites %}
{% for site in sites %}
- {{ site }}
{% endfor %}
{% else %}
- Site principal
{% endif %}

### 1.3 Responsable SMSI
**Nom:** {{ ciso_name }}
**Contact:** {{ ciso_email }}

## 2. Contexte de l'Organisation (Clause 4)

### 4.1 Compréhension de l'Organisation et de son Contexte

| Critère | Conforme | Non Conforme | N/A | Observations |
|---------|----------|--------------|-----|--------------|
| Analyse du contexte externe effectuée | ☐ | ☐ | ☐ | |
| Analyse du contexte interne effectuée | ☐ | ☐ | ☐ | |
| Facteurs influençant le SMSI identifiés | ☐ | ☐ | ☐ | |

### 4.2 Compréhension des Besoins et Attentes des Parties Intéressées

| Critère | Conforme | Non Conforme | N/A | Observations |
|---------|----------|--------------|-----|--------------|
| Parties intéressées identifiées | ☐ | ☐ | ☐ | |
| Exigences des parties intéressées documentées | ☐ | ☐ | ☐ | |
| Exigences légales et réglementaires identifiées | ☐ | ☐ | ☐ | |

### 4.3 Détermination du Périmètre du SMSI

| Critère | Conforme | Non Conforme | N/A | Observations |
|---------|----------|--------------|-----|--------------|
| Périmètre du SMSI défini et documenté | ☐ | ☐ | ☐ | |
| Limites et applicabilité du SMSI claires | ☐ | ☐ | ☐ | |
| Interfaces et dépendances identifiées | ☐ | ☐ | ☐ | |

### 4.4 Système de Management de la Sécurité de l'Information

| Critère | Conforme | Non Conforme | N/A | Observations |
|---------|----------|--------------|-----|--------------|
| SMSI établi et maintenu | ☐ | ☐ | ☐ | |
| Processus documentés | ☐ | ☐ | ☐ | |
| Amélioration continue démontrée | ☐ | ☐ | ☐ | |

## 3. Leadership (Clause 5)

### 5.1 Leadership et Engagement

| Critère | Conforme | Non Conforme | N/A | Observations |
|---------|----------|--------------|-----|--------------|
| Direction impliquée dans le SMSI | ☐ | ☐ | ☐ | |
| Politique de sécurité approuvée par la direction | ☐ | ☐ | ☐ | |
| Ressources allouées au SMSI | ☐ | ☐ | ☐ | |

### 5.2 Politique de Sécurité de l'Information

| Critère | Conforme | Non Conforme | N/A | Observations |
|---------|----------|--------------|-----|--------------|
| Politique adaptée au contexte de l'organisation | ☐ | ☐ | ☐ | |
| Politique communiquée aux parties pertinentes | ☐ | ☐ | ☐ | |
| Politique disponible et documentée | ☐ | ☐ | ☐ | |

### 5.3 Rôles, Responsabilités et Autorités

| Critère | Conforme | Non Conforme | N/A | Observations |
|---------|----------|--------------|-----|--------------|
| Rôles et responsabilités définis | ☐ | ☐ | ☐ | |
| Responsabilités du SMSI assignées | ☐ | ☐ | ☐ | |
| Communication des responsabilités | ☐ | ☐ | ☐ | |

## 4. Planification (Clause 6)

### 6.1 Actions face aux Risques et Opportunités

| Critère | Conforme | Non Conforme | N/A | Observations |
|---------|----------|--------------|-----|--------------|
| Processus d'évaluation des risques établi | ☐ | ☐ | ☐ | |
| Critères d'acceptation des risques définis | ☐ | ☐ | ☐ | |
| Évaluations des risques réalisées | ☐ | ☐ | ☐ | |
| Plan de traitement des risques documenté | ☐ | ☐ | ☐ | |
| Propriétaires des risques désignés | ☐ | ☐ | ☐ | |

### 6.2 Objectifs de Sécurité de l'Information

| Critère | Conforme | Non Conforme | N/A | Observations |
|---------|----------|--------------|-----|--------------|
| Objectifs cohérents avec la politique | ☐ | ☐ | ☐ | |
| Objectifs mesurables | ☐ | ☐ | ☐ | |
| Objectifs communiqués | ☐ | ☐ | ☐ | |
| Suivi des objectifs effectué | ☐ | ☐ | ☐ | |

### 6.3 Planification des Modifications

| Critère | Conforme | Non Conforme | N/A | Observations |
|---------|----------|--------------|-----|--------------|
| Processus de gestion des changements établi | ☐ | ☐ | ☐ | |
| Modifications planifiées et contrôlées | ☐ | ☐ | ☐ | |

## 5. Support (Clause 7)

### 7.1 Ressources

| Critère | Conforme | Non Conforme | N/A | Observations |
|---------|----------|--------------|-----|--------------|
| Ressources nécessaires déterminées | ☐ | ☐ | ☐ | |
| Ressources fournies | ☐ | ☐ | ☐ | |

### 7.2 Compétences

| Critère | Conforme | Non Conforme | N/A | Observations |
|---------|----------|--------------|-----|--------------|
| Compétences nécessaires déterminées | ☐ | ☐ | ☐ | |
| Personnel compétent | ☐ | ☐ | ☐ | |
| Formation dispensée | ☐ | ☐ | ☐ | |
| Enregistrements de compétence maintenus | ☐ | ☐ | ☐ | |

### 7.3 Sensibilisation

| Critère | Conforme | Non Conforme | N/A | Observations |
|---------|----------|--------------|-----|--------------|
| Personnel sensibilisé à la politique de sécurité | ☐ | ☐ | ☐ | |
| Personnel conscient de ses responsabilités | ☐ | ☐ | ☐ | |
| Conséquences de la non-conformité communiquées | ☐ | ☐ | ☐ | |

### 7.4 Communication

| Critère | Conforme | Non Conforme | N/A | Observations |
|---------|----------|--------------|-----|--------------|
| Communications internes et externes déterminées | ☐ | ☐ | ☐ | |
| Processus de communication établi | ☐ | ☐ | ☐ | |

### 7.5 Informations Documentées

| Critère | Conforme | Non Conforme | N/A | Observations |
|---------|----------|--------------|-----|--------------|
| Documentation requise par ISO 27001 présente | ☐ | ☐ | ☐ | |
| Documentation contrôlée | ☐ | ☐ | ☐ | |
| Documentation accessible | ☐ | ☐ | ☐ | |
| Gestion des versions effective | ☐ | ☐ | ☐ | |

## 6. Fonctionnement (Clause 8)

### 8.1 Planification et Contrôle Opérationnels

| Critère | Conforme | Non Conforme | N/A | Observations |
|---------|----------|--------------|-----|--------------|
| Processus nécessaires planifiés | ☐ | ☐ | ☐ | |
| Critères pour les processus établis | ☐ | ☐ | ☐ | |
| Contrôles mis en œuvre | ☐ | ☐ | ☐ | |

### 8.2 Appréciation des Risques

| Critère | Conforme | Non Conforme | N/A | Observations |
|---------|----------|--------------|-----|--------------|
| Évaluations des risques régulières | ☐ | ☐ | ☐ | |
| Résultats documentés | ☐ | ☐ | ☐ | |

### 8.3 Traitement des Risques

| Critère | Conforme | Non Conforme | N/A | Observations |
|---------|----------|--------------|-----|--------------|
| Plan de traitement mis en œuvre | ☐ | ☐ | ☐ | |
| Risques résiduels acceptés | ☐ | ☐ | ☐ | |
| Déclaration d'applicabilité (SOA) à jour | ☐ | ☐ | ☐ | |

## 7. Évaluation des Performances (Clause 9)

### 9.1 Surveillance, Mesure, Analyse et Évaluation

| Critère | Conforme | Non Conforme | N/A | Observations |
|---------|----------|--------------|-----|--------------|
| Indicateurs de performance définis | ☐ | ☐ | ☐ | |
| Surveillance régulière effectuée | ☐ | ☐ | ☐ | |
| Résultats analysés | ☐ | ☐ | ☐ | |

### 9.2 Audit Interne

| Critère | Conforme | Non Conforme | N/A | Observations |
|---------|----------|--------------|-----|--------------|
| Programme d'audit établi | ☐ | ☐ | ☐ | |
| Audits internes réalisés | ☐ | ☐ | ☐ | |
| Indépendance des auditeurs | ☐ | ☐ | ☐ | |
| Résultats communiqués à la direction | ☐ | ☐ | ☐ | |

### 9.3 Revue de Direction

| Critère | Conforme | Non Conforme | N/A | Observations |
|---------|----------|--------------|-----|--------------|
| Revues de direction régulières | ☐ | ☐ | ☐ | |
| Données d'entrée appropriées | ☐ | ☐ | ☐ | |
| Décisions et actions documentées | ☐ | ☐ | ☐ | |

## 8. Amélioration (Clause 10)

### 10.1 Non-conformité et Actions Correctives

| Critère | Conforme | Non Conforme | N/A | Observations |
|---------|----------|--------------|-----|--------------|
| Non-conformités traitées | ☐ | ☐ | ☐ | |
| Actions correctives mises en œuvre | ☐ | ☐ | ☐ | |
| Efficacité des actions évaluée | ☐ | ☐ | ☐ | |

### 10.2 Amélioration Continue

| Critère | Conforme | Non Conforme | N/A | Observations |
|---------|----------|--------------|-----|--------------|
| Opportunités d'amélioration identifiées | ☐ | ☐ | ☐ | |
| Amélioration continue du SMSI démontrée | ☐ | ☐ | ☐ | |

## 9. Contrôles de l'Annexe A

{% if controls %}
{% for control in controls %}
### {{ control.id }} - {{ control.title }}

| Critère | Conforme | Non Conforme | N/A | Observations |
|---------|----------|--------------|-----|--------------|
| Contrôle applicable et implémenté | ☐ | ☐ | ☐ | {{ control.notes }} |
| Preuves d'efficacité disponibles | ☐ | ☐ | ☐ | |

{% endfor %}
{% else %}
_Voir la Déclaration d'Applicabilité (SOA) pour le détail des 114 contrôles_
{% endif %}

## 10. Synthèse de l'Audit

### 10.1 Non-conformités Majeures
{% if major_findings %}
{% for finding in major_findings %}
- **{{ finding.id }}**: {{ finding.description }}
  - Clause: {{ finding.clause }}
  - Action requise: {{ finding.action }}
{% endfor %}
{% else %}
Aucune non-conformité majeure identifiée.
{% endif %}

### 10.2 Non-conformités Mineures
{% if minor_findings %}
{% for finding in minor_findings %}
- **{{ finding.id }}**: {{ finding.description }}
  - Clause: {{ finding.clause }}
  - Recommandation: {{ finding.recommendation }}
{% endfor %}
{% else %}
Aucune non-conformité mineure identifiée.
{% endif %}

### 10.3 Opportunités d'Amélioration
{% if improvements %}
{% for improvement in improvements %}
- {{ improvement }}
{% endfor %}
{% else %}
Aucune opportunité d'amélioration spécifique identifiée.
{% endif %}

## 11. Conclusion

### 11.1 Recommandation de l'Auditeur
{{ auditor_recommendation }}

### 11.2 Signatures

**Auditeur:**
Nom: {{ auditor_name }}
Date: {{ audit_date }}
Signature: ___________________________

**Responsable SMSI:**
Nom: {{ ciso_name }}
Date: _____________
Signature: ___________________________

---

**Document confidentiel - {{ organization_name }}**
**Date de génération:** {{ generation_date }}
