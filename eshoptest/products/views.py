from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model  # Import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from .forms import CheckoutForm
from .models import Item, OrderItem, Order, BillingAddress
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string

from eshopapp.models import CustomUser  


@login_required
def product_list(request):
    query = request.GET.get('q')
    if query:
        products = Item.objects.filter(title__icontains=query, is_active=True)
    else:
        products = Item.objects.filter(is_active=True)
    
    try:
        order = Order.objects.get(user=request.user, ordered=False)
    except Order.DoesNotExist:
        order = None

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/product_list_partial.html', {'products': products, 'order': order}, request=request)
        return JsonResponse({'html': html})

    # Debugging lines
    print(request.user.is_authenticated)  # This should print True if the user is authenticated
    print(request.user)  # Ensure user object is available
    print(get_user_model().objects.filter(email=request.user.email))  # Ensure user exists in the database
    print(request.user.email)  # Debugging line to ensure email is available

    return render(request, 'product_list.html', {'products': products, 'order': order, 'user': request.user})


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
    user = request.user
    try:
        order = Order.objects.get(user=user, ordered=False)
    except Order.DoesNotExist:
        order = None

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            if not order:
                order = Order(user=user, ordered=False, start_date=timezone.now())
                order.save()

            # Save the form data to the order's billing address
            billing_address = BillingAddress(
                user=user,
                street_address=form.cleaned_data.get('street_address'),
                apartment_address=form.cleaned_data.get('apartment_address'),
                country=form.cleaned_data.get('country'),
                zip=form.cleaned_data.get('zip'),
                address_type='B'
            )
            billing_address.save()
            order.billing_address = billing_address
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()
           
            admin_users = CustomUser.objects.filter(is_staff=True, is_superuser=True)
            for admin_user in admin_users:
                # Send confirmation email
                subject = 'Order Confirmation'
                plain_message = 'New order created.'
                from_email = 'from@example.com'
                to_email = admin_user.email
                html_message = render_to_string('order_confirmation_email.html', {'order': order})
                send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

            return redirect('products:order_confirmation')
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

def order_confirmation(request):
    user = request.user
    order = Order.objects.filter(user=user, ordered=True).latest('ordered_date')
    return render(request, 'order_confirmation.html', {'order': order})