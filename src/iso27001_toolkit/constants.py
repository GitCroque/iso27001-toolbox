"""
Constantes utilisées dans l'application ISO 27001 Toolkit
"""

# ============================================================================
# Gestion des risques
# ============================================================================

# Échelle de scoring des risques (1-5)
RISK_SCORE_MIN = 1
RISK_SCORE_MAX = 5

# Matrice des risques (5x5)
RISK_MATRIX_SIZE = 5

# Seuils de niveau de risque (basés sur le score = impact × vraisemblance)
RISK_THRESHOLD_CRITICAL = 20  # Score >= 20: Critique (16-25)
RISK_THRESHOLD_HIGH = 16      # Score >= 16: Élevé (16-19)
RISK_THRESHOLD_MEDIUM = 10    # Score >= 10: Moyen (10-15)
# Score < 10: Faible (1-9)

# Niveaux de risque
RISK_LEVEL_CRITICAL = 'critical'
RISK_LEVEL_HIGH = 'high'
RISK_LEVEL_MEDIUM = 'medium'
RISK_LEVEL_LOW = 'low'

# Catégories de risques
RISK_CATEGORY_CONFIDENTIALITY = 'confidentiality'
RISK_CATEGORY_INTEGRITY = 'integrity'
RISK_CATEGORY_AVAILABILITY = 'availability'
RISK_CATEGORY_COMPLIANCE = 'compliance'

# Statuts de traitement des risques
RISK_STATUS_IDENTIFIED = 'identified'
RISK_STATUS_ANALYZED = 'analyzed'
RISK_STATUS_TREATED = 'treated'
RISK_STATUS_ACCEPTED = 'accepted'
RISK_STATUS_MONITORING = 'monitoring'

# Options de traitement des risques
RISK_TREATMENT_MITIGATE = 'mitigate'
RISK_TREATMENT_ACCEPT = 'accept'
RISK_TREATMENT_TRANSFER = 'transfer'
RISK_TREATMENT_AVOID = 'avoid'

# Périodes de révision des risques (en jours)
RISK_REVIEW_PERIOD_CRITICAL = 30   # Mensuel pour risques critiques
RISK_REVIEW_PERIOD_HIGH = 90       # Trimestriel pour risques élevés
RISK_REVIEW_PERIOD_MEDIUM = 180    # Semestriel pour risques moyens
RISK_REVIEW_PERIOD_LOW = 365       # Annuel pour risques faibles

# ============================================================================
# Contrôles ISO 27001
# ============================================================================

# Statuts d'implémentation des contrôles
CONTROL_STATUS_NOT_STARTED = 'not_started'
CONTROL_STATUS_IN_PROGRESS = 'in_progress'
CONTROL_STATUS_IMPLEMENTED = 'implemented'
CONTROL_STATUS_VERIFIED = 'verified'

# Niveaux de priorité des contrôles
CONTROL_PRIORITY_LOW = 'low'
CONTROL_PRIORITY_MEDIUM = 'medium'
CONTROL_PRIORITY_HIGH = 'high'
CONTROL_PRIORITY_CRITICAL = 'critical'

# Catégories de contrôles ISO 27001:2022 Annexe A
CONTROL_CATEGORY_ORGANIZATIONAL = 'A.5'  # 37 contrôles organisationnels
CONTROL_CATEGORY_PEOPLE = 'A.6'          # 8 contrôles des personnes
CONTROL_CATEGORY_PHYSICAL = 'A.7'        # 14 contrôles physiques
CONTROL_CATEGORY_TECHNOLOGICAL = 'A.8'   # 34 contrôles technologiques

# Nombre total de contrôles par catégorie
CONTROL_COUNT_ORGANIZATIONAL = 37
CONTROL_COUNT_PEOPLE = 8
CONTROL_COUNT_PHYSICAL = 14
CONTROL_COUNT_TECHNOLOGICAL = 34
CONTROL_COUNT_TOTAL = 114

# ============================================================================
# Audit et conformité
# ============================================================================

# Score de préparation à l'audit
AUDIT_READINESS_EXCELLENT = 90   # >= 90%: Excellent
AUDIT_READINESS_GOOD = 75        # >= 75%: Bon
AUDIT_READINESS_FAIR = 60        # >= 60%: Acceptable
AUDIT_READINESS_POOR = 40        # >= 40%: Insuffisant
# < 40%: Critique

# Pondération du score de préparation
AUDIT_SCORE_WEIGHT_CONTROLS = 0.7  # 70% basé sur les contrôles
AUDIT_SCORE_WEIGHT_DOCS = 0.3      # 30% basé sur la documentation

# Types d'audit
AUDIT_TYPE_INTERNAL = 'internal'
AUDIT_TYPE_EXTERNAL = 'external'
AUDIT_TYPE_CERTIFICATION = 'certification'
AUDIT_TYPE_SURVEILLANCE = 'surveillance'

# ============================================================================
# Politiques de sécurité
# ============================================================================

# Types de politiques
POLICY_TYPES = [
    'information_security_policy',
    'access_control_policy',
    'asset_management_policy',
    'cryptography_policy',
    'physical_security_policy',
    'operations_security_policy',
    'communications_security_policy',
    'supplier_relationships_policy',
    'incident_management_policy',
    'business_continuity_policy',
    'compliance_policy',
]

# Cycle de révision des politiques (en jours)
POLICY_REVIEW_PERIOD = 365  # Révision annuelle

# ============================================================================
# Configuration système
# ============================================================================

# Limites de taille de fichiers
MAX_LOG_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
MAX_LOG_BACKUP_COUNT = 5

# Timeouts (en secondes)
DEFAULT_TIMEOUT = 30

# ============================================================================
# Messages et affichage
# ============================================================================

# Couleurs pour les niveaux de risque
RISK_COLOR_MAP = {
    RISK_LEVEL_LOW: 'green',
    RISK_LEVEL_MEDIUM: 'yellow',
    RISK_LEVEL_HIGH: 'red',
    RISK_LEVEL_CRITICAL: 'bold red',
}

# Couleurs pour les statuts de contrôles
CONTROL_STATUS_COLOR_MAP = {
    CONTROL_STATUS_NOT_STARTED: 'red',
    CONTROL_STATUS_IN_PROGRESS: 'yellow',
    CONTROL_STATUS_IMPLEMENTED: 'green',
    CONTROL_STATUS_VERIFIED: 'bold green',
}

# Couleurs pour les statuts de risques
RISK_STATUS_COLOR_MAP = {
    RISK_STATUS_IDENTIFIED: 'yellow',
    RISK_STATUS_ANALYZED: 'cyan',
    RISK_STATUS_TREATED: 'green',
    RISK_STATUS_ACCEPTED: 'blue',
    RISK_STATUS_MONITORING: 'magenta',
}
