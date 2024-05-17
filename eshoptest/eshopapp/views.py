from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    """
    Display the view for logging in users.
    This function handles logging in users. It renders the login.html
    template, which contains the corresponding form. If a user submits the login form,
    it validates the form data and logs in the user if the credentials are correct.
    """
    login_form = AuthenticationForm()

    if 'login' in request.POST:
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            # authenticate user using the provided credentials
            user = authenticate(username=login_form.cleaned_data['username'], 
                                password=login_form.cleaned_data['password'])
            if user is not None:
                # log in the user
                auth_login(request, user)

                # redirect to product list after successful login
                return redirect('products:product_list')

    return render(request, 'login.html', {
        'login_form': login_form,
    })


@login_required
# Ensure that the user is logged in to access this view
def welcome_view(request):
    """
    Display the welcome view for authenticated users.
    This function renders the welcome.html template, which includes user information
    such as their username. It is only accessible to authenticated users.
    """
    return render(request, 'welcome.html', {'user': request.user})


def logout_view(request):
    """
        Log out the current user and redirect to the login view.
        This function logs out the currently authenticated user using Django's
        authentication system and redirects them to the login view for signing in.
        """
    auth_logout(request)
    return redirect('login')
