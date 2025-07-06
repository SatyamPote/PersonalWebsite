from django.contrib import admin
from django.urls import path
from portfolio_api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('api/user-data/', views.user_data, name='user_data'),  # ✅ THIS LINE
]
