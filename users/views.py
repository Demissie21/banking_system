from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from core.models import BankAccount
import random

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create bank account
            account_number = str(random.randint(100000000000, 999999999999))
            BankAccount.objects.create(user=user, account_number=account_number, balance=0)
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "users/signup.html", {"form": form})

# Signup view
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after signup
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "users/signup.html", {"form": form})

# Custom login view
def custom_login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
    return render(request, "users/login.html")

# Dashboard view (protected)
@login_required
def dashboard_view(request):
    return render(request, "users/dashboard.html", {"user": request.user})
