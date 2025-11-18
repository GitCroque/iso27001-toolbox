"""
Exceptions personnalisées pour ISO 27001 Toolkit
"""


class ISO27001ToolkitError(Exception):
    """Classe de base pour toutes les exceptions du toolkit"""
    pass


class ConfigurationError(ISO27001ToolkitError):
    """Erreur liée à la configuration"""
    pass


class ValidationError(ISO27001ToolkitError):
    """Erreur de validation des données utilisateur"""
    pass


class TemplateError(ISO27001ToolkitError):
    """Erreur lors du rendu des templates"""
    pass


class DataPersistenceError(ISO27001ToolkitError):
    """Erreur lors de la sauvegarde/chargement des données"""
    pass


class ControlNotFoundError(ISO27001ToolkitError):
    """Contrôle ISO 27001 non trouvé"""
    pass


class RiskNotFoundError(ISO27001ToolkitError):
    """Risque non trouvé dans le registre"""
    pass


class PolicyNotFoundError(ISO27001ToolkitError):
    """Politique non trouvée"""
    pass


class EncryptionError(ISO27001ToolkitError):
    """Erreur lors du chiffrement/déchiffrement"""
    pass


class AuditError(ISO27001ToolkitError):
    """Erreur lors de la préparation d'audit"""
    pass
