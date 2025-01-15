from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from . import forms
from .models import Ticket


@login_required
def ticket_create(request):
    form = forms.TicketForm()
    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    return render(request, 'review/create_ticket.html', context={'form': form})

@login_required
def ticket_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'review/view_posts.html', {'ticket': ticket})

@login_required
def ticket_edit(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    if request.method == "POST":
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
    return render(request, 'review/edit_ticket_page.html', context={'edit_form': edit_form})

@login_required
def review_create(request):
    review_form = forms.ReviewForm()
    ticket_form = forms.TicketForm()
    if request.method == "POST":
        review_form = forms.ReviewForm(request.POST, request.FILES)
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if all([review_form.is_valid(), ticket_form.is_valid()]):
            review = review_form.save(commit=False)
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
    context = {'review_form': review_form, 'ticket_form': ticket_form}
    return render(request, 'review/create_review.html', context=context)
