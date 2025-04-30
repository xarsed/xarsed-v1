from django import template

register = template.Library()

@register.filter
def replace_underscore(value):

    name = value.replace("_", " ")
    
    return name