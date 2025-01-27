from django import template

register = template.Library()


@register.filter
def model_type(instance):
    return type(instance).__name__


@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if user == context["user"]:
        return "Vous avez"
    return user.username + " a"


@register.simple_tag(takes_context=True)
def get_poster_name(context, user):
    if user == context["user"]:
        return "Vous"
    return user.username


@register.filter
def range_filter(value):
    return range(value)


@register.filter
def is_array_filled(array):
    return len(array) > 0
