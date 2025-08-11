from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

# Import register view from your app
from core.views import register_view  # Replace 'core' with your actual app name

# Custom Login View
def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

# Dashboard View
def dashboard_view(request):
    return HttpResponse("Welcome to your dashboard!")

# Home Page View
def home_view(request):
    return HttpResponse("Welcome to the Banking System!")

# URL Patterns
urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('register/', register_view, name='register'),
    path('login/', custom_login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', include('django.contrib.auth.urls')),  # Logout and auth routes
    path('api/', include('core.urls')),  # API views from your app
    path('api-auth/', include('rest_framework.urls')),  # Browsable API login/logout
]
