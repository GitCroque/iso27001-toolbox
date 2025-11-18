# Évaluation des Risques de Sécurité de l'Information

**Organisation:** {{ organization_name }}
**Date d'évaluation:** {{ assessment_date }}
**Version:** {{ version }}
**Responsable:** {{ risk_owner }}

## 1. Résumé Exécutif

### 1.1 Contexte
Cette évaluation des risques a été réalisée dans le cadre de la démarche de certification ISO 27001 de {{ organization_name }}.

### 1.2 Méthodologie
L'évaluation utilise une matrice de risques 5x5 basée sur :
- **Impact** : Évaluation de la gravité des conséquences (1-5)
- **Vraisemblance** : Probabilité d'occurrence (1-5)
- **Score de risque** : Impact × Vraisemblance

### 1.3 Échelle de Criticité
- **Critique** (20-25) : Action immédiate requise
- **Élevé** (16-19) : Attention prioritaire
- **Moyen** (10-15) : Surveillance active
- **Faible** (1-9) : Surveillance de routine

## 2. Périmètre de l'Évaluation

### 2.1 Actifs Couverts
{% if assets %}
{% for asset in assets %}
- {{ asset }}
{% endfor %}
{% else %}
- Systèmes d'information
- Données clients et employés
- Infrastructure réseau
- Applications métier
{% endif %}

### 2.2 Période Couverte
Du {{ start_date }} au {{ end_date }}

## 3. Registre des Risques

{% if risks %}
{% for risk in risks %}
### {{ risk.id }} - {{ risk.name }}

**Catégorie:** {{ risk.category }}
**Statut:** {{ risk.status }}

**Description:**
{{ risk.description }}

**Actifs Concernés:**
{% for asset in risk.assets %}
- {{ asset }}
{% endfor %}

**Évaluation:**
- Impact: {{ risk.impact }}/5
- Vraisemblance: {{ risk.likelihood }}/5
- **Score de risque: {{ risk.risk_score }}**
- **Niveau: {{ risk.risk_level }}**

**Traitement:**
{% if risk.treatment == 'mitigate' %}
Réduction du risque par mise en place de contrôles
{% elif risk.treatment == 'accept' %}
Acceptation du risque
{% elif risk.treatment == 'transfer' %}
Transfert du risque (assurance, externalisation)
{% elif risk.treatment == 'avoid' %}
Évitement du risque
{% endif %}

**Mesures de Mitigation:**
{% for measure in risk.mitigation_measures %}
- {{ measure }}
{% endfor %}

**Contrôles ISO 27001 Associés:**
{% for control in risk.controls %}
- {{ control }}
{% endfor %}

**Responsable:** {{ risk.owner }}
**Date de Revue:** {{ risk.review_date }}

---

{% endfor %}
{% else %}
Aucun risque identifié dans le registre.
{% endif %}

## 4. Synthèse des Risques

### 4.1 Répartition par Niveau de Risque

| Niveau | Nombre | Pourcentage |
|--------|--------|-------------|
| Critique | {{ stats.critical }} | {{ stats.critical_percent }}% |
| Élevé | {{ stats.high }} | {{ stats.high_percent }}% |
| Moyen | {{ stats.medium }} | {{ stats.medium_percent }}% |
| Faible | {{ stats.low }} | {{ stats.low_percent }}% |
| **Total** | **{{ stats.total }}** | **100%** |

### 4.2 Répartition par Catégorie

| Catégorie | Nombre |
|-----------|--------|
| Confidentialité | {{ stats.confidentiality }} |
| Intégrité | {{ stats.integrity }} |
| Disponibilité | {{ stats.availability }} |
| Conformité | {{ stats.compliance }} |

### 4.3 Répartition par Traitement

| Traitement | Nombre |
|------------|--------|
| Réduction | {{ stats.mitigate }} |
| Acceptation | {{ stats.accept }} |
| Transfert | {{ stats.transfer }} |
| Évitement | {{ stats.avoid }} |

## 5. Plan d'Action

### 5.1 Actions Prioritaires

Les risques critiques et élevés nécessitent une attention immédiate :

{% if priority_risks %}
{% for risk in priority_risks %}
1. **{{ risk.id }}** - {{ risk.name }}
   - Échéance: {{ risk.deadline }}
   - Responsable: {{ risk.owner }}
   - Actions: {{ risk.actions }}
{% endfor %}
{% endif %}

### 5.2 Calendrier de Révision

- **Prochaine révision complète:** {{ next_review_date }}
- **Révision des risques critiques:** Mensuelle
- **Révision des risques élevés:** Trimestrielle
- **Révision des autres risques:** Annuelle

## 6. Conclusion

### 6.1 État Actuel
{{ organization_name }} a identifié {{ stats.total }} risques de sécurité de l'information.

### 6.2 Recommandations
1. Prioriser le traitement des risques critiques et élevés
2. Mettre en place les contrôles de sécurité recommandés
3. Maintenir une surveillance continue des risques
4. Réviser régulièrement l'évaluation des risques

---

**Document confidentiel - {{ organization_name }}**
**Date de génération:** {{ generation_date }}
