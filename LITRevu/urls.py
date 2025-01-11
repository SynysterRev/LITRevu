"""
URL configuration for LITRevu project.

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
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

import authentication.views
from authentication.forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', authentication.views.signup, name='signup'),
    path('login/', LoginView.as_view(
        template_name='authentication/login.html',
        authentication_form=LoginForm,
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', authentication.views.home, name='home'),
]
