# portfolio_project/urls.py

from django.contrib import admin
from django.urls import path
from content.views import portfolio_data_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/data/', portfolio_data_api, name='api-data'),
]

# The static files configuration for MEDIA_URL has been removed.
# It is not needed when hosting images on an external service like Postimage.me.