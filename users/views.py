from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Account
import random

# Utility function for generating account numbers
def generate_account_number():
    return str(random.randint(100000000000, 999999999999))

# Signup view
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after signup
            # Create a bank account for the user
            Account.objects.create(user=user, account_number=generate_account_number(), balance=0)
            messages.success(request, "Signup successful! Bank account created.")
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "users/signup.html", {"form": form})

# Custom login view
def custom_login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Invalid username or password"
    return render(request, 'users/login.html', {'error': error})

# Dashboard view (protected)
@login_required
def dashboard_view(request):
    account = None
    if hasattr(request.user, 'account'):
        account = request.user.account
    return render(request, "users/dashboard.html", {"user": request.user, "account": account})
