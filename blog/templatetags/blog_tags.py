from django import template
from blog.models import *

register = template.Library()


@register.simple_tag(name='get_categories')
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('blog/sidebar-navigation.html')
def sidebar_navigation(category_selected='all'):
    return {'categories': Category.objects.all(), 'category_selected': category_selected}
