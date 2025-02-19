"""
URL configuration for travel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, permissions
from listings.views import BookingViewSet

router = routers.DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='booking')
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Travel API",  # Customize your API title
      default_version='v1',  # Set your API version
      description="Your API description", # Customize your API description
      terms_of_service="https://www.example.com/terms/",  # Add terms of service URL (optional)
      contact=openapi.Contact(email="contact@amanabiy.com"),  # Add contact information (optional)
      license=openapi.License(name="MIT License"),
   ),
   public=True,  # Set to False for production to restrict access
   permission_classes=(permissions.AllowAny,), # Or your custom permission classes
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # ReDoc UI (optional)
]