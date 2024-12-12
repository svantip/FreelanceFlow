from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import LoginForm, RegistrationForm


@login_required
def home_view(request):
    """
    Display the home page for logged-in users.
    """
    return render(request, 'home.html')


def login_view(request):
    """
    Handle user login functionality.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                # Redirect to home after successful login
                return redirect('myapp:home')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'authentication/login.html', {'form': form})


def register_view(request):
    """
    Handle user registration functionality.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            messages.success(
                request, "Registration successful! You can now log in.")
            # Redirect to login after registration
            return redirect('myapp:login')
    else:
        form = RegistrationForm()

    return render(request, 'authentication/register.html', {'form': form})
