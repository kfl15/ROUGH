"""
URL configuration for crm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views as v

# Router creates API URLs automatically for the ViewSet.
router = DefaultRouter() # an empty automatic url maker

# This creates list/create/detail/update/delete URLs for registrations.
router.register('registrations', v.RegistrationViewSet)

urlpatterns = [
    path('registration/', v.register,name='signup'),
    path('login/', v.login,name='login'),
    path('customer/', v.show_customer,name='customer'),
    path('customer/edit/<int:cid>', v.edit_customer,name='customer_edit'),
    path('customer/delete/<int:cid>', v.delete_customer,name='customer_delete'),
    path('customer/bill', v.show_customer_bill,name='customer_bill'),
    path('api/', include(router.urls)),
    path('api/login/', v.LoginAPIView.as_view(), name='api_login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profile/', v.ProfileAPIView.as_view(), name='api_profile'),
]
# /api/login/ → checks credentials and returns tokens.
# /api/token/refresh/ → accepts a refresh token and returns a new access token.
# .as_view() makes the class-based view usable by Django URLs.
# without thise paths, the login & refresh APIs can not be accessed.

