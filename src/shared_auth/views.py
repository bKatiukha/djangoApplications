from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from src.blog.utils import DataMixin
from .forms import *


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
        UserProfile.objects.create(user=user)
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


def edit_profile(request):
    user = request.user
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, request.FILES, instance=profile)

        # UserProfile.objects.create(user=user)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            if not profile:
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
            else:
                profile_form.save()

            return redirect('blog')
    else:
        user_form = UserEditForm(instance=request.user)
        if profile:
            profile_form = UserProfileEditForm(instance=profile)
        else:
            profile_form = UserProfileEditForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Edit profile'
    }
    return render(request, 'shared/edit_user.html', context)
