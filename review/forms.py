from django import forms

from review import models
from widgets.widgets import TitleInputWidget, TextAreaWidget, TicketImageWidget


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget = TitleInputWidget(
            attrs={'placeholder': "Titre", 'type': "text", 'max_length': self.fields['title'].max_length})
        self.fields['description'].widget = TextAreaWidget(attrs={'placeholder': "Description", 'max_length':
            self.fields['description'].max_length})
        self.fields['image'].widget = TicketImageWidget(attrs={'placeholder': "Image"})


class ReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'ticket', 'body']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['headline'].widget = TitleInputWidget(
            attrs={'placeholder': "Titre", 'type': "text", 'max_length': self.fields['headline'].max_length})
        self.fields['body'].widget = TextAreaWidget(
            attrs={'placeholder': "Commentaire", 'max_length': self.fields['body'].max_length})
        self.fields['image'].widget = TicketImageWidget(attrs={'placeholder': "Image"})
