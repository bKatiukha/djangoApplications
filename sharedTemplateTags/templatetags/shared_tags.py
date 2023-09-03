from django import template
from shared.consts.navigation import NAVIGATION_ITEMS

register = template.Library()


@register.inclusion_tag('shared/main_navigation.html')
def main_navigation():
    return {"navItems": NAVIGATION_ITEMS}


