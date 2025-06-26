from django.contrib import admin
from django.urls import path
from content.views import portfolio_data_api

# NEW: Import these for serving media files
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/data/', portfolio_data_api, name='api-data'),
]

# NEW: Add this line to serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)