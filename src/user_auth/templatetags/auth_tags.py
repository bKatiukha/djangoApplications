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
    },
    {
        'title': 'Oryx statistic',
        'routerLink': 'oryx_losses_statistics'
    }
]


@register.inclusion_tag('user_auth/main_navigation.html')
def main_navigation():
    return {"navItems": NAVIGATION_ITEMS}


