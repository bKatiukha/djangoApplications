from django.db.models import Count, Q

from .models import Category


class DataMixin:
    paginate_by = 4

    def get_user_context(self, **kwargs):
        context = kwargs
        categories = Category.objects.annotate(
            total=Count('post', filter=Q(post__is_published=True))).filter(total__gt=0)
        context['categories'] = categories

        if not self.request.user.is_authenticated:
            print('not authorize')

        if 'category_selected' not in context:
            context['category_selected'] = 'all'
        return context
