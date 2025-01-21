from itertools import chain

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from authentication.models import User
from . import forms, models
from .models import Ticket, Review


@login_required
def home(request):
    current_user = request.user
    user_reviews = models.Review.objects.filter(user=current_user).select_related('user')
    user_tickets = models.Ticket.objects.filter(user=current_user).select_related('user')
    followed_reviews = models.Review.objects.filter(user__in=current_user.followed.all()).select_related('user')
    followed_tickets = models.Ticket.objects.filter(user__in=current_user.followed.all()).select_related('user')
    other_reviews =  models.Review.objects.filter(ticket__in=user_tickets).select_related('user')
    reviews_and_tickets = sorted(chain(user_reviews, user_tickets, followed_reviews, followed_tickets, other_reviews),
                                 key=lambda x: x.time_created, reverse=True)
    paginator = Paginator(reviews_and_tickets, 1)
    number_page = request.GET.get('page')
    page_obj = paginator.get_page(number_page)

    context = {
        'page_obj': page_obj,
        'total_pages': paginator.num_pages,
    }
    return render(request, 'review/home.html', context=context)


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
    reviews = models.Review.objects.filter(user=request.user).order_by('-time_created').select_related('user')
    tickets = models.Ticket.objects.filter(user=request.user).order_by('-time_created').select_related('user')
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
    following = request.user.following.all().select_related('followed_user')
    following_usernames = [follow.followed_user.username for follow in following]
    followers = request.user.followed_by.all().select_related('user')
    followers_usernames = [follower.user.username for follower in followers]
    form = forms.FollowUserForm(user=request.user)
    if request.method == "POST":
        form = forms.FollowUserForm(request.POST, user=request.user)
        if form.is_valid():
            user = get_object_or_404(User, username=form.cleaned_data['username'])
            request.user.followed.add(user)
            return redirect('following')
    context = {
        'following_usernames': following_usernames,
        'followers': followers_usernames,
        'form': form,
    }

    return render(request, 'review/following.html', context=context)


@login_required
def unfollow_user(request, username):
    followed_user = get_object_or_404(User, username=username)
    if request.method == "POST":
        request.user.followed.remove(followed_user)
        return redirect('following')
    # followed_user

# @login_required
# def review_view(request, review_id):
#     review = get_object_or_404(models.Review, id=review_id)
#     return render(request, 'review/view_posts.html', {'review': review})
