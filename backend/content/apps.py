from django.apps import AppConfig

# We move the logic outside the class to avoid certain startup issues.
def create_superuser_on_startup():
    """
    Checks if a superuser needs to be created and does so without
    crashing if the database isn't ready.
    """
    from django.contrib.auth import get_user_model
    from django.db import utils
    import os

    User = get_user_model()
    
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'localpassword')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@example.com')

    try:
        # Check if the user already exists.
        if not User.objects.filter(username=ADMIN_USERNAME).exists():
            print(f"--- Superuser '{ADMIN_USERNAME}' not found. Creating... ---")
            User.objects.create_superuser(
                username=ADMIN_USERNAME,
                password=ADMIN_PASSWORD,
                email=ADMIN_EMAIL
            )
            print(f"--- Superuser '{ADMIN_USERNAME}' created successfully! ---")
        else:
            print(f"--- Superuser '{ADMIN_USERNAME}' already exists. Skipping. ---")
    except utils.OperationalError as e:
        # This can happen if the database isn't fully migrated yet.
        print(f"--- DB not ready, skipping superuser creation: {e} ---")
    except Exception as e:
        print(f"--- An unexpected error occurred during superuser creation: {e} ---")


class ContentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'content'

    def ready(self):
        # We only run this logic if the 'createsuperuser' command is NOT being run,
        # and we are on a production-like server.
        import sys
        is_gunicorn = "gunicorn" in sys.argv[0]
        
        # This check is crucial to prevent the logic from running during migrations
        is_migrating = 'migrate' in sys.argv
        
        if is_gunicorn and not is_migrating:
            create_superuser_on_startup()