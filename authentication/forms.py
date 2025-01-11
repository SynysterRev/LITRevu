from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django import forms
from widgets.widgets import InputWidget, PasswordWidget


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = InputWidget(attrs={'placeholder': "Nom d'utilisateur"})

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=InputWidget(attrs={'placeholder': "Nom d'utilisateur"}))
    password = forms.CharField(widget=PasswordWidget(attrs={'placeholder': "Mot de passe"}))
