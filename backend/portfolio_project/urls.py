from django.contrib import admin
from django.urls import path
from content.views import portfolio_data_api

# --- ADD THESE TWO IMPORTS ---
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/data/', portfolio_data_api, name='api-data'),
]

# --- ADD THIS LINE AT THE END ---
# This is required to serve files from MEDIA_ROOT in development and production
# when using Render Disks.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)