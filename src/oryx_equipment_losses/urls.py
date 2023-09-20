from django.urls import path
from django.conf.urls.static import static
from app_config import settings

from .views import *

urlpatterns = [
    path('', oryx_equipment_losses, name='oryx_equipment_losses'),
    path('force_update_oryx_losses', force_update_oryx_losses, name='force_update_oryx_losses'),
    path('oryx_losses_statistics', oryx_losses_statistics, name='oryx_losses_statistics'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
