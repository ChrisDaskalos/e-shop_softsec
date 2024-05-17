# eshopapp/urls.py

from django.urls import path
from .views import login_view, logout_view, welcome_view
from products.views import (
    OrderSummaryView,
    ItemDetailView,
    checkout_view,
    add_to_cart,
    remove_from_cart,
    product_list  # Ensure this is imported
)

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('welcome/', welcome_view, name='welcome'),
    path('checkout/', checkout_view, name='checkout'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('products/', product_list, name='product_list'),
]
