from django.urls import path
from .views import (
    OrderSummaryView,
    ItemDetailView,
    checkout_view,
    add_to_cart,
    remove_from_cart,
    product_list,
    order_confirmation  # Import the order_confirmation view
)

app_name = 'products'

urlpatterns = [
    path('', product_list, name='product_list'),  # Root URL for the products app
    path('checkout/', checkout_view, name='checkout'),
    path('product/<int:pk>/', ItemDetailView.as_view(), name='product'),  # Use pk for product detail view
    path('add-to-cart/<int:pk>/', add_to_cart, name='add-to-cart'),  # Use pk for add-to-cart
    path('remove-from-cart/<int:pk>/', remove_from_cart, name='remove-from-cart'),  # Use pk for remove-from-cart
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('order-confirmation/', order_confirmation, name='order_confirmation'),  # Added order-confirmation URL
]
