"""pharmacy_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('pharmashop.urls')),
  
    path('api/v1/',  include('djoser.urls.jwt')),  
    # To login, the URL should be api/v1/jwt/create/
    # To refresh the token, the URL should be api/v1/jwt/refresh/
    # To verify the token, the URL should be api/v1/jwt/verify/
    # this website lienk can help https://djoser.readthedocs.io/en/latest/jwt_endpoints.html

  
]
