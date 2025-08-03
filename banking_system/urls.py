from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_api(request):
    return redirect('/api/')

urlpatterns = [
    path('', redirect_to_api),  # Redirect root to /api/
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),  # Your app's URLs are under /api/
]
