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
    path("admin/", admin.site.urls),
    path("signup/", authentication.views.signup, name="signup"),
    path(
        "",
        LoginView.as_view(
            template_name="authentication/login.html",
            authentication_form=LoginForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("home/", review.views.home, name="home"),
    path("posts/", review.views.view_posts, name="posts_view"),
    path("review/create", review.views.review_create, name="review_create"),
    path(
        "ticket/<int:ticket_id>/review/create/",
        review.views.review_answer_create,
        name="review_answer_create",
    ),
    path("review/<int:review_id>/edit/", review.views.review_edit, name="review_edit"),
    path(
        "review/<int:review_id>/delete/",
        review.views.delete_review,
        name="review_delete",
    ),
    path("ticket/create", review.views.ticket_create, name="ticket_create"),
    path("ticket/<int:ticket_id>/edit/", review.views.ticket_edit, name="ticket_edit"),
    path(
        "ticket/<int:ticket_id>/delete/",
        review.views.delete_ticket,
        name="ticket_delete",
    ),
    path("following/", review.views.following_users, name="following"),
    path("unfollow/<str:username>/", review.views.unfollow_user, name="unfollow"),
    path("search/", review.views.search_user, name="search"),
    path("follow/", review.views.follow_user, name="follow"),
    path(
        "update-profile-picture/",
        authentication.views.update_profile_picture,
        name="update_profile_picture",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
