from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.http import HttpResponse

# Define a simple homepage view
def home_view(request):
    return HttpResponse("Welcome to the Banking System!")

urlpatterns = [
    # Homepage
    path('', home_view, name='home'),

    # Admin
    path('admin/', admin.site.urls),

    # Authentication
    path('signup/', user_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # API
    path('api/', include('core.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
