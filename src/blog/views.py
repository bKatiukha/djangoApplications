from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.shortcuts import redirect, render
from .forms import CustomAddPostForm, AddPostForm
from .models import *
from .utils import *


class BlogHomePage(DataMixin, ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Home')
        return dict(list(context.items()) + list(context_def.items()))

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class BlogCategoryPage(DataMixin, ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'posts'
    allow_empty = False
    # extra_context = {'category_selected': 'all'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        category_slug = self.kwargs['category_slug']
        context_def = self.get_user_context(
            title=category_slug + ' posts',
            category_selected=category_slug
        )
        return dict(list(context.items()) + list(context_def.items()))
        # context['category_selected'] = self.kwargs['category_slug']
        # return context

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['category_slug'], is_published=True)


class BlogPostPage(LoginRequiredMixin, DataMixin, DetailView):
    model = Post
    template_name = 'blog/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    # pk_url_kwarg = 'pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(
            title=self.kwargs['post_slug'],
        )
        return dict(list(context.items()) + list(context_def.items()))


class AddFormViewPostFormPage(DataMixin, FormView):
    form_class = CustomAddPostForm
    template_name = 'blog/form-view-add-page-form.html'
    success_url = reverse_lazy('blog')
    # raise_exception = True # 403 page

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(
            title='add post form',
            category_selected='form_view_add_post',
        )
        return dict(list(context.items()) + list(context_def.items()))

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        Post.objects.create(**form.cleaned_data)
        return redirect('blog')


# @login_required
def show_custom_add_page_form(request):
    if request.method == 'POST':
        form = CustomAddPostForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            try:
                Post.objects.create(**form.cleaned_data)
                return redirect('blog')
            except:
                form.add_error(None, 'Form validation error')
    else:
        form = CustomAddPostForm()

    context = {
        'form': form,
        'category_selected': 'form_view_add_post'
    }
    return render(request, 'blog/form-view-add-page-form.html', context=context)


# LoginRequiredMixin
class AddPostFormPage(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'blog/add-page-form.html'
    success_url = reverse_lazy('blog')
    login_url = reverse_lazy('blog')
    # raise_exception = True # 403 page

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(
            title='add post form',
            category_selected='add_post'
        )
        return dict(list(context.items()) + list(context_def.items()))


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>404</h1>')
