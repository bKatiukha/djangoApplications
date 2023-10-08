from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from app_config import settings
from src.blog.views import page_not_found
from src.user_auth.views import *

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Django DRF API Documentation",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Include DRF-Swagger URLs
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


    path('admin/', admin.site.urls, name='admin'),
    path('', RedirectView.as_view(url=reverse_lazy('blog')), name='home'),
    path('login/', LoginUserPage.as_view(), name='login'),
    path('register/', RegisterUserPage.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('profile/', include('src.user_auth.urls')),
    path('blog/', include('src.blog.urls'), name='blog'),
    path('web_rtc/', include('src.web_rtc.urls'), name='web_rtc'),
    path('chat/', include('src.chat.urls'), name='chat'),
    path('oryx_equipment_losses/', include('src.oryx_equipment_losses.urls'), name='oryx_equipment_losses'),
    path('api/', include([
        path('blog/', include('src.api.blog.urls'), name='blog_api'),
        path('auth/', include('src.api.user_auth.urls'), name='auth_api'),
        path('oryx/', include('src.api.oryx.urls'), name='oryx'),
        path('chat/', include('src.api.chat.urls'), name='chat')
    ])),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls"))
    ]

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
                   static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found
