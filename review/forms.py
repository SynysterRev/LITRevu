from django import forms

from review import models
from widgets.widgets import TitleInputWidget, TextAreaWidget, TicketImageWidget, RadioSelectWidget


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget = TitleInputWidget(
            attrs={'title': "Titre", 'type': "text", 'max_length': self.fields['title'].max_length})
        self.fields['description'].widget = TextAreaWidget(attrs={'title': "Description", 'max_length':
            self.fields['description'].max_length})
        self.fields['image'].widget = TicketImageWidget(attrs={'title': "Image"})


class ReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['headline'].widget = TitleInputWidget(
            attrs={'title': "Titre", 'type': "text", 'max_length': self.fields['headline'].max_length})
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
