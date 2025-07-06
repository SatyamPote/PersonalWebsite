from django.urls import path
from .views import user_data

urlpatterns = [
    path('user-data/', user_data),
]
