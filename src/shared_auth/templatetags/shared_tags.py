from django import template

register = template.Library()

NAVIGATION_ITEMS = [
    {
        'title': 'Blog',
        'routerLink': 'blog'
    },
    {
        'title': 'WebRTC',
        'routerLink': 'web_rtc'
    },
    {
        'title': 'Chat',
        'routerLink': 'chat'
    },
    {
        'title': 'Oryx parser',
        'routerLink': 'oryx_equipment_losses'
    }
]


@register.inclusion_tag('shared/main_navigation.html')
def main_navigation():
    return {"navItems": NAVIGATION_ITEMS}


