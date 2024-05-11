from django.contrib import admin
from django.urls import path, include
from eshopapp.views import hello_world, log_in, sign_up  # Adjust if your views are organized differently

urlpatterns = [
    path('admin/', admin.site.urls),
    path('eshop/', include('eshopapp.urls')),  # Assuming you have other URLs handled in the app
    path('', hello_world, name='home'),  # This routes the root URL to your view
    path('login/', log_in, name='login'),
    path('signup/', sign_up, name='signup'),
]
