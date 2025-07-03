from django.urls import path
from .views import DashboardDataView

urlpatterns = [
    path('ds/', DashboardDataView.as_view(), name='dashboard-data'),
]
