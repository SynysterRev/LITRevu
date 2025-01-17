from django import forms

from authentication.models import User
from review import models
from widgets.widgets import TitleInputWidget, TextAreaWidget, TicketImageWidget, RadioSelectWidget, InputSearchWidget


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget = TitleInputWidget(
            attrs={'title': "Titre", 'type_input': "text", 'max_length': self.fields['title'].max_length})
        self.fields['description'].widget = TextAreaWidget(attrs={'title': "Description", 'max_length':
            self.fields['description'].max_length})
        self.fields['image'].widget = TicketImageWidget(attrs={'title': "Image"})


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['headline'].widget = TitleInputWidget(
            attrs={'title': "Titre", 'type_input': "text", 'max_length': self.fields['headline'].max_length})
        self.fields['body'].widget = TextAreaWidget(
            attrs={'title': "Commentaire", 'max_length': self.fields['body'].max_length})
        self.fields['rating'].widget = RadioSelectWidget(choices=[
            (0, '0'),
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
        ], attrs={'title': "Note"})


class FollowUserForm(forms.Form):
    username = forms.CharField(max_length=100,
                               widget=InputSearchWidget(attrs={'placeholder': "Nom d'utilisateur", 'type_input': "text",
                                                               'max_length': '100'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("L'utilisateur %(username)s n'existe pas.", code='not_found',
                                        params={'username': username})
        if user == self.user:
            raise forms.ValidationError("Vous ne pouvez pas vous suivre vous-même.", code='invalid')

        following = self.user.followed.all()
        if user in following:
            raise forms.ValidationError("Vous suivez déjà cet utilisateur.", code='already_followed')
        return user
