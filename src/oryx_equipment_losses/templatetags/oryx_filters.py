from django import template

register = template.Library()


@register.simple_tag(name='get_nested_value')
def get_nested_value(dictionary, *keys):
    """
    Custom template filter to access values within nested dictionaries.
    """

    value = dictionary
    for key in keys:
        try:
            value = value[key]
        except (TypeError, KeyError):
            return None

    return value
