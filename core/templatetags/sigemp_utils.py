from django import template
from django.utils.html import escape

register = template.Library()


@register.filter
def getattr(obj, attr):
    if hasattr(obj, attr):
        value = getattr(obj, attr)
        if callable(value):
            value = value()
        return value
    return ""


@register.filter
def getattr_safe(obj, attr):
    value = getattr(obj, attr)
    if callable(value):
        value = value()
    return escape(str(value))
