# PersonalWebsite/backend/api/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('ds/', views.test_api),  # Or your actual view name
]
