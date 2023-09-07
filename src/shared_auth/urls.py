from django.urls import path
from django.conf.urls.static import static
from app_config import settings
from src.shared_auth.views import edit_profile

urlpatterns = [
    path('', edit_profile, name='edit_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
