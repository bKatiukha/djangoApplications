from django import template

register = template.Library()

NAVIGATION_ITEMS = [
    {
        'title': 'blog',
        'routerLink': 'blog'
    },
    {
        'title': 'blog',
        'routerLink': 'blog'
    },
    {
        'title': 'jinja',
        'routerLink': 'jinja'
    },
    {
        'title': 'jinja',
        'routerLink': 'jinja'
    }
]


@register.inclusion_tag('shared/main_navigation.html')
def main_navigation():
    return {"navItems": NAVIGATION_ITEMS}


