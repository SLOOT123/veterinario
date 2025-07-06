from django import template

register = template.Library()

@register.filter
def dict_get(dictionary, key):
    return dictionary.get(key, '')

@register.filter
def to(start, end):
    return range(start, end + 1)
