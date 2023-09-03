from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from blog.utils import DataMixin
from sharedTemplateTags.forms import RegisterUserForm, LoginUserForm


class RegisterUserPage(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'shared/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Registration')
        return dict(list(context.items()) + list(context_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('blog')


class LoginUserPage(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'shared/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Login')
        return dict(list(context.items()) + list(context_def.items()))

    def get_success_url(self):
        return reverse_lazy('blog')


def logout_user(request):
    logout(request)
    return redirect('login')


# def register_page(request):  # HttpRequest
#     context = {
#         'title': 'registration'
#     }
#     return render(request, 'shared/login.html', context=context)


# def login_page(request):  # HttpRequest
#     # post = get_object_or_404(Post, slug=post_slug)
#     context = {
#         'title': 'login'
#     }
#     return render(request, 'shared/login.html', context=context)
