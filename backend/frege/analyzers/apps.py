from django.apps import AppConfig


class AnalyzersConfig(AppConfig):
    """
    Configuration class for the 'frege.analyzers' Django application.

    This class defines the configuration for the 'analyzers' app, setting 
    the default auto field type and the app's name for proper integration 
    within the Django project.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "frege.analyzers"
