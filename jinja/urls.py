from django.urls import path
from django.conf.urls.static import static
from djangoApplications import settings

from jinja.views import jinja

urlpatterns = [
    path('', jinja, name='jinja'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
