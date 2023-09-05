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


# class CustomAddPostFormPage(CreateView):
#     form_class = CustomAddPostForm
#     template_name = 'blog/form-view-add-page-form.html'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['category_selected'] = 'form_view_add_post'
    #     return context
    #

class AddFormViewPostFormPage(DataMixin, FormView):
    form_class = CustomAddPostForm
    template_name = 'blog/form-view-add-page-form.html'
    success_url = reverse_lazy('blog')
    # login_url = reverse_lazy('blog')
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


# def show_blog(request):  # HttpRequest
#     posts = Post.objects.filter(is_published=True)
#     paginator = Paginator(posts, 4)
#
#     page_number = request.GET.get('page')
#     if not page_number:
#         page_number = 1
#     page_posts = paginator.page(page_number)
#     print(page_posts)
#     context = {
#         'posts': page_posts,
#         'paginator': page_posts.paginator,
#         'page_obj': page_posts,
#         'category_selected': 'all'
#     }
#     return render(request, 'blog/blog.html', context=context)


# def show_category(request, category_slug):  # HttpRequest
#     context = {
#         'posts': Post.objects.filter(category__slug=category_slug),
#         'category_selected': category_slug
#     }
#     return render(request, 'blog/category.html', context=context)


# def show_post(request, post_slug):  # HttpRequest
#     post = get_object_or_404(Post, slug=post_slug)
#     context = {
#         'post': post
#     }
#     return render(request, 'blog/post.html', context=context)


# def show_add_page_form(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         print(form.is_valid())
#         if form.is_valid():
#             form.save()
#             return redirect('blog')
#     else:
#         form = AddPostForm()
#
#     context = {
#         'form': form,
#         'category_selected': 'add_post'
#     }
#     return render(request, 'blog/add-page-form.html', context=context)
