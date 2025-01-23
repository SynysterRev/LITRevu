import base64
import json

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import render, redirect

from authentication.forms import SignupForm


def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})


@login_required
def update_profile_picture(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        profile_picture = json_data.get('profile_picture')
        format, imgstr = profile_picture.split(';base64,')
        ext = format.split('/')[-1]
        image_data = ContentFile(base64.b64decode(imgstr), name=f"profile.{ext}")
        if image_data:
            user = request.user
            user.profile_picture = image_data
            user.save()
            return JsonResponse({"success": True,
                                 "new_image_url": user.profile_picture.url})
    return JsonResponse({"success": False}, status=400)

# json_data = json.loads(request.body)
#         username = json_data.get('username')
#         followed_user = get_object_or_404(User, username=username)
#         if followed_user:
#             request.user.followed.add(followed_user)
#             return JsonResponse({"status": "success"})
#     return JsonResponse({"status": "invalid_request"}, status=400)
