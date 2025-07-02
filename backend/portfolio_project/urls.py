<<<<<<< HEAD
# portfolio_project/urls.py
=======
>>>>>>> parent of 0bbc509 (Refactor portfolio backend and frontend integration)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('', include('content.urls')), # Include content app's URLs at the root
=======
    path('api/', include('content.urls')), 
>>>>>>> parent of 0bbc509 (Refactor portfolio backend and frontend integration)
]