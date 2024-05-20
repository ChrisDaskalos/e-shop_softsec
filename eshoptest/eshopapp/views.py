from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django_ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='4/m', block=True, method='POST')
def login_view(request):
    """
    Display the view for logging in users.
    This function handles logging in users. It renders the login.html
    template, which contains the corresponding form. If a user submits the login form,
    it validates the form data and logs in the user if the credentials are correct.
    """
    login_form = AuthenticationForm()
    
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            # Authenticate user using the provided credentials
            user = authenticate(username=login_form.cleaned_data['username'], 
                                password=login_form.cleaned_data['password'])
            if user is not None:
                # Log in the user
                auth_login(request, user)
                # Redirect to product list after successful login
                return redirect('products:product_list')
            else:
                messages.error(request, 'Invalid username or password.', extra_tags='login-error')
        else:
            messages.error(request, 'Invalid username or password.', extra_tags='login-error')

    return render(request, 'login.html', {
        'login_form': login_form,
    })


def logout_view(request):
    """
    Log out the current user and redirect to the login view.
    This function logs out the currently authenticated user using Django's
    authentication system and redirects them to the login view for signing in.
    """
    auth_logout(request)
    return redirect('login')
