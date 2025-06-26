from django.apps import AppConfig

# The file is now clean and simple, as it should be for a production app.
class ContentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'content'

    # The 'ready' method has been removed.