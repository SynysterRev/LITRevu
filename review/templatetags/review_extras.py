from django import template
from django.template.defaultfilters import date as _date

register = template.Library()

@register.filter
def model_type(instance):
    return type(instance).__name__