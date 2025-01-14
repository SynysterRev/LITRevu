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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

import authentication.views
import review.views
from authentication.forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', authentication.views.signup, name='signup'),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        authentication_form=LoginForm,
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', authentication.views.home, name='home'),
    path('ticket/create', review.views.ticket_create, name='ticket_create'),
    path('review/create', review.views.review_create, name='review_create'),
    path('ticket/<int:ticket_id>/', review.views.ticket_view, name='ticket_view'),
    path('ticket/<int:ticket_id>/edit/', review.views.ticket_edit, name='ticket_edit'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
