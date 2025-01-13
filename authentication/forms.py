from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django import forms
from widgets.widgets import InputWidget


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = InputWidget(attrs={'placeholder': "Nom d'utilisateur", 'type': "text"})
        self.fields['password1'].widget = InputWidget(attrs={'placeholder': "Mot de passe", 'type': "password"})
        self.fields['password2'].widget = InputWidget(attrs={'placeholder': "Confirmer le mot de passe",
                                                             'type': "password"})

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=InputWidget(attrs={'placeholder': "Nom d'utilisateur",'type': "text"}))
    password = forms.CharField(widget=InputWidget(attrs={'placeholder': "Mot de passe", 'type': "password"}),
                               error_messages={'required': "Ce champ est obligatoire"})
