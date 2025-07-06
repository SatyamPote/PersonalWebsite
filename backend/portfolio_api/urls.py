# portfolio_api/urls.py

from django.urls import path
from .views import index, user_data

urlpatterns = [
    path('', index, name='index'),
    path('user-data/', user_data, name='user-data'),
]
