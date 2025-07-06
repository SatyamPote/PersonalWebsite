from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home_view(request):
    return JsonResponse({"message": "Backend is running"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('api/', include('portfolio_api.urls')),  # ✅ updated name
]
