from django.forms import Widget, PasswordInput
from django.template import loader
from django.utils.safestring import mark_safe


class InputWidget(Widget):
    template_name = 'widgets/input_widget.html'

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)

class PasswordWidget(PasswordInput):
    template_name = 'widgets/password_widget.html'

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)

