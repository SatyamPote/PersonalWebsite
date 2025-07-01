from django.urls import path
from . import views

urlpatterns = [
    path('data/', views.portfolio_data_api, name='portfolio-data-api'),
]