from django.apps import AppConfig
import os
import sys

class ContentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'content'

    # This 'ready' method is a hook that runs once when the Django app starts.
    # We will use it to create your admin user on the live server.
    def ready(self):
        # We need to check if the server is actually running.
        # This prevents the code from executing during other commands like 'makemigrations'.
        # 'gunicorn' is the command Render uses to run your live server.
        is_running_server = 'gunicorn' in sys.argv

        if is_running_server:
            # We must import the User model inside this method.
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            # These lines read your credentials from the secure Environment Variables on Render.
            # If the variables aren't found, it uses default values (for local testing).
            ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
            ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'localpassword')
            ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@example.com')

            # This logic checks if a user table is empty.
            if not User.objects.exists():
                print("--- No users found in the database. Creating superuser... ---")
                try:
                    User.objects.create_superuser(
                        username=ADMIN_USERNAME,
                        password=ADMIN_PASSWORD,
                        email=ADMIN_EMAIL
                    )
                    print(f"--- Superuser '{ADMIN_USERNAME}' created successfully! ---")
                except Exception as e:
                    print(f"--- CRITICAL ERROR: Could not create superuser: {e} ---")
            else:
                # On subsequent deploys, this message will show, which is correct.
                print("--- Users already exist. Skipping superuser creation. ---")