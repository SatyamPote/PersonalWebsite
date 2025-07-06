from django.urls import path
from . import views

urlpatterns = [
    path('user-data/', views.user_data, name='user-data'),
]
