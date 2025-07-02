from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('content.urls')),       # Serves frontend or main site
    path('api/', include('content.urls')),   # Optional: also serve API from /api/
]
