from django import template
from django.template.defaultfilters import date as _date

register = template.Library()

@register.filter
def model_type(instance):
    return type(instance).__name__

@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if user == context['user']:
        return "vous avez"
    return user.username + "a"

@register.filter
def range_filter(value):
    return range(value)
