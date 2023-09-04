"""
URL configuration for app_config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from app_config import settings
from src.blog.views import page_not_found
from src.shared_auth.views import *

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', RedirectView.as_view(url=reverse_lazy('blog')), name='home'),
    path('login/', LoginUserPage.as_view(), name='login'),
    path('register/', RegisterUserPage.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('blog/', include('src.blog.urls'), name='blog'),
    path('jinja/', include('src.jinja.urls'), name='jinja'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
                   static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found
