from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django import forms
from widgets.widgets import InputWidget


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = InputWidget(attrs={'title': "Nom d'utilisateur", 'type_input': "text"})
        self.fields['password1'].widget = InputWidget(attrs={'title': "Mot de passe", 'type_input': "password"})
        self.fields['password2'].widget = InputWidget(attrs={'title': "Confirmer le mot de passe",
                                                             'type_input': "password"})

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=InputWidget(attrs={'title': "Nom d'utilisateur",'type_input': "text"}))
    password = forms.CharField(widget=InputWidget(attrs={'title': "Mot de passe", 'type_input': "password"}),
                               error_messages={'required': "Ce champ est obligatoire"})
