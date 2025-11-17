"""
Exceptions personnalisées pour ISO 27001 Toolkit
"""


class ISO27001ToolkitError(Exception):
    """Exception de base pour l'application"""
    pass


class ValidationError(ISO27001ToolkitError):
    """Erreur de validation des données"""
    pass


class ControlNotFoundError(ISO27001ToolkitError):
    """Contrôle non trouvé"""
    def __init__(self, control_id: str):
        self.control_id = control_id
        super().__init__(f"Contrôle non trouvé: {control_id}")


class RiskNotFoundError(ISO27001ToolkitError):
    """Risque non trouvé"""
    def __init__(self, risk_id: str):
        self.risk_id = risk_id
        super().__init__(f"Risque non trouvé: {risk_id}")


class TemplateNotFoundError(ISO27001ToolkitError):
    """Template non trouvé"""
    def __init__(self, template_name: str):
        self.template_name = template_name
        super().__init__(f"Template non trouvé: {template_name}")


class ConfigurationError(ISO27001ToolkitError):
    """Erreur de configuration"""
    pass


class DataError(ISO27001ToolkitError):
    """Erreur de données"""
    pass


class ExportError(ISO27001ToolkitError):
    """Erreur lors de l'export"""
    pass


class ImportError(ISO27001ToolkitError):
    """Erreur lors de l'import"""
    pass
