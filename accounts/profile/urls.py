from django.http import HttpResponse
from django.urls import path

def profile_redirect(request):
    return HttpResponse("This is your profile page placeholder.")

urlpatterns = [
    path('accounts/profile/', profile_redirect, name='profile'),
]
