# content/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # This maps the root URL '/' to your index view
    path('api/user-data/', views.portfolio_data_api, name='portfolio_data_api'),
]