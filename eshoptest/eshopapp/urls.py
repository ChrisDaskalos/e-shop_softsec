from django.urls import path
from .views import hello_world, log_in, sign_up # Import the view from the current app

urlpatterns = [
    path('', hello_world, name='home'),  # This sets up the root of the app URL namespace to your view
    path('login/', log_in, name='login'),
    path('signup/', sign_up, name='signup'),
]
