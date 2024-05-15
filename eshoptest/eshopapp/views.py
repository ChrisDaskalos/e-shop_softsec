from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm  # Custom sign-up form
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

def unified_view(request):
    signup_form = CustomUserCreationForm()
    login_form = AuthenticationForm()

    if request.method == 'POST':
        if 'signup' in request.POST:
            signup_form = CustomUserCreationForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                auth_login(request, user)
                return redirect('checkout')  # Redirect to welcome page after successful signup
        elif 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = authenticate(username=login_form.cleaned_data['username'], 
                                    password=login_form.cleaned_data['password'])
                if user is not None:
                    auth_login(request, user)
                    return redirect('checkout')  # Redirect to welcome page after successful login

    return render(request, 'unified.html', {
        'signup_form': signup_form,
        'login_form': login_form,
    })

@login_required
def welcome_view(request):
    # Render the welcome page and include user information
    return render(request, 'welcome.html', {'user': request.user})

def logout_view(request):
    auth_logout(request)
    return redirect('unified')  # Redirect to unified view after logging out
