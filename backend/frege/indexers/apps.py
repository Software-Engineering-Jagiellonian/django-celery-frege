from django.apps import AppConfig

class IndexersConfig(AppConfig):
    """
    Configuration class for the 'indexers' app within the 'frege' Django project.

    This class sets the default auto field type for models in the app to 'BigAutoField',
    which provides 64-bit integers for automatically incrementing primary keys.

    Attributes:
        default_auto_field (str): Specifies the default type for auto-created primary keys.
        name (str): The full Python path to the app, used by Django to identify the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "frege.indexers"
