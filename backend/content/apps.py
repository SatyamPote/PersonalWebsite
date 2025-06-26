from django.apps import AppConfig
import os
import sys

class ContentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'content'

    def ready(self):
        is_running_server = 'gunicorn' in sys.argv
        if is_running_server:
            from django.contrib.auth import get_user_model
            from django.db import utils
            User = get_user_model()
            
            ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
            ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'localpassword')
            ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@example.com')

            try:
                if not User.objects.filter(username=ADMIN_USERNAME).exists():
                    print(f"--- Creating superuser '{ADMIN_USERNAME}'... ---")
                    User.objects.create_superuser(
                        username=ADMIN_USERNAME,
                        password=ADMIN_PASSWORD,
                        email=ADMIN_EMAIL
                    )
                    print(f"--- Superuser '{ADMIN_USERNAME}' created successfully. ---")
                else:
                    print(f"--- Superuser '{ADMIN_USERNAME}' already exists. Skipping. ---")
            except utils.OperationalError as e:
                print(f"--- DB not ready, skipping superuser creation: {e} ---")
            except Exception as e:
                print(f"--- An unexpected error occurred: {e} ---")