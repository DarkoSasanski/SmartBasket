"""Domasna5 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from Domasna5 import settings
from SmartBasket.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name="index"),
    path("index", index, name="index"),
    path("login-cust", login_customer, name="login-cust"),
    path("login-sale", login_salesman, name="login-sale"),
    path("login-del", login_deliveryman, name="login-del"),
    path("register-cust", register_customer, name="register-cust"),
    path("register-sale", register_salesman, name="register-sale"),
    path("register-del", register_deliveryman, name="register-del"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
