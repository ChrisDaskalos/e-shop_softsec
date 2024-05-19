from django.contrib import admin
from django.urls import path, include
from eshopapp import views as eshopapp_views  # Adjust the import as necessary
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('eshopapp.urls')),  # Main app URLs
    path('products/', include('products.urls', namespace='products')),  # Products app URLs
    path('login/', eshopapp_views.login_view, name='login'),  # Login view URL
]

# Add this line to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
