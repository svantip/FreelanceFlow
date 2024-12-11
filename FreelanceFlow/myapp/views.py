from django.shortcuts import render , redirect
from django.http import HttpResponse
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password  # Import za proveru heširane lozinke
from django.contrib.auth.decorators import login_required

## Create your views here.
def index(request):
    return render(request, 'index.html')

def home_view(request):
    """
    Prikazuje početnu stranicu i proverava da li je korisnik prijavljen.
    """
    context = {
        'is_authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else None
    }
    return render(request, 'base.html', context)
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Pokušaj da pronađeš korisnika sa tim username-om
            try:
                user = User.objects.get(Username=username)
            except User.DoesNotExist:
                messages.error(request, "Invalid username or password!")
                return redirect('myapp:login')

            # Provera lozinke sa heširanjem
            if check_password(password, user.Password):  # Koristi check_password da proveriš lozinku
                # Ako je lozinka ispravna, kreiraj sesiju za korisnika
                request.session['user_id'] = user.ID_User
                messages.success(request, f"Welcome, {username}!")
                return redirect('myapp:home')  # Zameni 'home' sa tvojim URL-om
            else:
                messages.error(request, "Invalid username or password!")
                return redirect('myapp:login')  # Ponovo prikazivanje login stranice
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})
def logout_view(request):
    request.session.flush()  # Briše sve podatke iz sesije
    messages.success(request, "Logged out successfully!")
    return redirect('login')  # Zameni 'login' sa tvojim URL-om za prijavu


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('home')  # Zameni 'login' sa tvojim URL-om za prijavu
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})