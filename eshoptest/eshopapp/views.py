from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, LogInForm


def hello_world(request):
    return render(request, 'eshopapp/home.html')


def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace 'index' with your desired redirect URL
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LogInForm()
    return render(request, 'login.html', {'form': form})


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Replace 'index' with your desired redirect URL
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})