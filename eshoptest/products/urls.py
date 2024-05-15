from django.urls import path
from .views import (
    OrderSummaryView,
    ItemDetailView,
    checkout_view,
    add_to_cart,
    remove_from_cart
)

app_name = 'products'

urlpatterns = [
    path('checkout/', checkout_view, name='checkout'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
]
