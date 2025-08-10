from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),            # your app's routes
    path('api-auth/', include('rest_framework.urls')),  # ✅ Add this line
]
