from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from . import forms


@login_required
def ticket_create(request):
    form = forms.CreateTicketForm()
    if request.method == "POST":
        form = forms.CreateTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            if 'image' in request.FILES:
                print("Image reçue:", request.FILES['image'])
            else:
                print("Aucune image reçue.")
            ticket.save()
            return redirect('home')
    return render(request, 'review/create_ticket.html', context={'form': form})
