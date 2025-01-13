from django import forms

from review import models
from widgets.widgets import TitleInputWidget, TextAreaWidget, TicketImageWidget


class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget = TitleInputWidget(attrs={'placeholder': "Titre", 'type': "text"})
        self.fields['description'].widget = TextAreaWidget(attrs={'placeholder': "Description"})
        self.fields['image'].widget = TicketImageWidget(attrs={'placeholder': "Image"})
