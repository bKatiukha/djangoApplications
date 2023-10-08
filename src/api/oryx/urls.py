from django.urls import path

from src.api.oryx.views import LossesStatisticsAPIView

urlpatterns = [
    path('losses/', LossesStatisticsAPIView.as_view(), name='losses'),
]
