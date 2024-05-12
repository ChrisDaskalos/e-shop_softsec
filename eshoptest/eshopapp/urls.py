from django.urls import path
from .views import unified_view, logout_view, welcome_view

urlpatterns = [
    path('', unified_view, name='unified'),
    path('logout/', logout_view, name='logout'),
    path('welcome/', welcome_view, name='welcome'),
]
