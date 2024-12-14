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
                return redirect('myapp:home')
            else:
                # Add a non-field error for invalid credentials
                form.add_error(None, "Invalid username or password.")
        else:
            # Log form errors for debugging purposes
            print("Form errors:", form.errors)
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
                request, "Registration successful! You can now log in."
            )
            # Redirect to login after registration
            return redirect('myapp:login')
        else:
            print(form.errors)  # Debugging: Print errors in the console
    else:
        form = RegistrationForm()

    return render(request, 'authentication/register.html', {'form': form})
