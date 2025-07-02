from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Home route
    path('user-data/', views.user_data, name='user-data'),  # ✅ FIXED this line
]
