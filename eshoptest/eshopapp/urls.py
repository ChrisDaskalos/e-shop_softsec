from django.urls import path
from .views import hello_world  # Import the view from the current app

urlpatterns = [
    path('', hello_world, name='home'),  # This sets up the root of the app URL namespace to your view
]
