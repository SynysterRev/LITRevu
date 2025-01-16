from itertools import chain

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from . import forms, models
from .models import Ticket, Review
from authentication.models import User, UserFollows


@login_required
def home(request):
    photo_data = {
        'photo_1': 'https://picsum.photos/seed/1/300/200',
        'photo_2': 'https://picsum.photos/seed/2/300/400',
        'photo_3': 'https://picsum.photos/seed/3/300/300',
        'photo_4': 'https://picsum.photos/seed/4/300/300',
        'photo_5': 'https://picsum.photos/seed/5/300/300',
        'photo_6': 'https://picsum.photos/seed/6/300/300',
        'photo_7': 'https://picsum.photos/seed/7/300/400',
        'photo_8': 'https://picsum.photos/seed/8/300/300',
        'photo_9': 'https://picsum.photos/seed/9/300/200',
        'photo_10': 'https://picsum.photos/seed/10/300/100',
        'photo_11': 'https://picsum.photos/seed/11/300/400',
        'photo_12': 'https://picsum.photos/seed/12/300/400',
    }
    return render(request, 'review/home.html', photo_data)


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


# @login_required
# def ticket_view(request, ticket_id):
#     ticket = get_object_or_404(Ticket, id=ticket_id)
#     return render(request, 'review/view_posts.html', {'ticket': ticket})


@login_required
def ticket_edit(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.user != request.user:
        return redirect('home')
    edit_form = forms.TicketForm(instance=ticket)
    if request.method == "POST":
        edit_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('home')
    return render(request, 'review/edit_ticket_page.html', context={'edit_form': edit_form})


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id, user=request.user)
    if request.method == "POST":
        ticket.delete()
        return redirect('posts_view')


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


@login_required
def review_answer_create(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    review_form = forms.ReviewForm()
    if request.method == "POST":
        review_form = forms.ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            print(review)
            return redirect('home')
    context = {'review_form': review_form, 'ticket': ticket}
    return render(request, 'review/create_review_answer.html', context=context)


@login_required
def review_edit(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    edit_form = forms.ReviewForm(instance=review)
    if request.method == "POST":
        edit_form = forms.ReviewForm(request.POST, request.FILES, instance=review)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('home')
    context = {'edit_form': edit_form, 'ticket': review.ticket}
    return render(request, 'review/edit_review_page.html', context=context)


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id, user=request.user)
    if request.method == "POST":
        review.delete()
        return redirect('posts_view')


@login_required
def view_posts(request):
    reviews = models.Review.objects.filter(user=request.user).order_by('-time_created')
    tickets = models.Ticket.objects.filter(user=request.user).order_by('-time_created')
    reviews_and_tickets = sorted(chain(reviews, tickets), key=lambda x: x.time_created, reverse=True)
    paginator = Paginator(reviews_and_tickets, 5)
    number_page = request.GET.get('page')
    page_obj = paginator.get_page(number_page)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'review/view_posts.html', context=context)


@login_required
def following_users(request):
    following = request.user.followed.all()
    followers = request.user.followed_by.all()
    followers_usernames = [follower.username for follower in followers]
    context = {
        'following': following,
        'followers': followers_usernames,
    }
    return render(request, 'review/following.html', context=context)

# @login_required
# def review_view(request, review_id):
#     review = get_object_or_404(models.Review, id=review_id)
#     return render(request, 'review/view_posts.html', {'review': review})
