from django import template

register = template.Library()

@register.filter(name='username_part')
def username_part(value):
    """Extracts the part of the username before the '@' and strips any whitespace."""
    if value:
        return value.split('@')[0].strip()
    return ''
