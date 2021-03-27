"""SuccessPJT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls import include
from django.conf import settings
from SuccessPJT import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', RedirectView.as_view(url='/main/')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup', views.CreateUserView.as_view(), name='signup'),
    path('accounts/login/done', views.RegisterdView.as_view(), name= 'create_user_done'),
    path('accounts/password_resets/', views.pwreset, name='reset'),
]
