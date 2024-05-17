from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from .forms import CheckoutForm
from .models import Item, OrderItem, Order, BillingAddress


@login_required
def product_list(request):
    """
    View for displaying a list of products available for purchase.
    Retrieves active products from the database and renders them on the product list template.
    If the user has an active order, it retrieves the order to display alongside the products.
    Returns:
        HttpResponse: Rendered product list template with products and user's active order.
    """
    # querying active products from the database
    products = Item.objects.filter(is_active=True)
    try:
        # Trying to get the user's active order
        order = Order.objects.get(user=request.user, ordered=False)
    # Handling the case if the order does not exist
    except Order.DoesNotExist:
        order = None
    # Rendering the product list template with products and order
    return render(request, 'product_list.html', {'products': products, 'order': order})


class OrderSummaryView(LoginRequiredMixin, View):
    """
    View for displaying the summary of the user's order.

    Retrieves the user's active order and renders the order summary template with the order details.

    Attributes:
        model: Specifies the model used for the view.
        template_name: Specifies the template used for rendering the view.
    """
    def get(self, *args, **kwargs):
        try:
            # Trying to get the user's active order
            order = Order.objects.get(user=self.request.user, ordered=False)
            # Creating context dictionary with order object
            context = {
                'object': order
            }
            # Rendering the order summary template with context
            return render(self.request, 'order_summary.html', context)
        # Handling the case if the order does not exist
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            # Redirecting to home page
            return redirect("/")


class ItemDetailView(DetailView):
    """
    View for displaying detailed information about a specific product.

    Attributes:
        model: Specifies the model used for the view.
        template_name: Specifies the template used for rendering the view.
    """
    # Setting the model for the view
    model = Item
    # Setting the template for the view
    template_name = "product-detail.html"


@login_required
def checkout_view(request):
    """
   View for handling the checkout process.

   Retrieves the user's active order and renders the checkout template with the checkout form.
   Processes the form data upon submission and redirects to the order confirmation page.

   Returns:
       HttpResponse: Rendered checkout template with the checkout form.
   """
    # Getting the current user
    user = request.user
    try:
        # Trying to get the user's active order
        order = Order.objects.get(user=user, ordered=False)
    # Handling the case if the order does not exist
    except Order.DoesNotExist:
        order = None

    if request.method == 'POST':
        # Creating a form instance with POST data
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Process the form data and save the shipping details
            # Redirect to a confirmation page or perform any other actions
            return redirect('order_confirmation')
    # Handling the case if the request method is not POST
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {'order': order, 'form': form})


@login_required
def add_to_cart(request, pk):
    """
    View for adding an item to the user's shopping cart.

    Retrieves the selected item from the database and adds it to the user's active order.
    Increments the quantity if the item is already in the cart.

    Returns:
        HttpResponseRedirect: Redirects to the product list page.
    """
    # Retrieves the item object from the database based on the provided primary key
    item = get_object_or_404(Item, pk=pk)
    # Retrieves or creates an order item associated with the user and the selected item
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    # Queries the user's active order
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    # Checks if the user has an active order
    if order_qs.exists():
        # Retrieves the first active order
        order = order_qs[0]
        # Checks if the item is already in the user's cart
        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item quantity was updated.")
        else:
            order.items.add(order_item)
            messages.info(request, "Item was added to your cart.")
    else:
        ordered_date = timezone.now()
        # Creates a new order for the user
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        # Adds the order item to the new order
        order.items.add(order_item)
        messages.info(request, "Item was added to your cart.")
    return redirect("products:product_list")


@login_required
def remove_from_cart(request, pk):
    """
    View for removing an item from the user's shopping cart.

    Retrieves the selected item from the database and removes it from the user's active order.

    Returns:
        HttpResponseRedirect: Redirects to the product list page.
    """
    # Retrieves the item object from the database based on the provided primary key
    item = get_object_or_404(Item, pk=pk)
    # Queries the user's active order
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    # Checks if the user has an active order
    if order_qs.exists():
        # Retrieves the first active order
        order = order_qs[0]
        # Checks if the item is in the user's cart
        if order.items.filter(item__pk=item.pk).exists():
            # Retrieves the order item associated with the user and the selected item
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "Item was removed from your cart.")
        else:
            messages.info(request, "This item was not in your cart")
    else:
        messages.info(request, "You do not have an active order")
    return redirect("products:product_list")


@login_required
def order_summary(request):
    """
    View for displaying the summary of the user's order.

    Retrieves the user's active order and renders the order summary template with the order details.

    Returns:
        HttpResponse: Rendered order summary template with the order details.
    """
    try:
        # Retrieves the user's active order
        order = Order.objects.get(user=request.user, ordered=False)
        context = {
            'order': order
        }
        # Renders the order summary template with the order details
        return render(request, 'order_summary.html', context)
    except Order.DoesNotExist:
        messages.info(request, "You do not have an active order")
        return redirect("/")
