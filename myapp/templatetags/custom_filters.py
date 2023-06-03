from django import template

register = template.Library()

@register.filter(name='getattr')
def custom_getattr(obj, attr_name):
    return getattr(obj, attr_name)