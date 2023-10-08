from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.oryx.serializers import LossSerializer, GroupedLossesSerializer
from src.oryx_equipment_losses.models import Report


class LossesStatisticsAPIView(APIView):
    def get(self, request):
        reports = Report.objects.prefetch_related(
            'report_losses',
            'report_losses__vehicle__vehicle_category',
            'report_losses__vehicle__country_made_icon'
        ).all()

        formatted_losses = []
        for report in reports:
            for loss in report.report_losses.all():
                formatted_losses.append({
                    "name": loss.name,
                    "side": loss.side,
                    "category": loss.vehicle.vehicle_category.name,
                    "vehicle": loss.vehicle.name,
                    "report_date": str(report.report_date),
                    "country_made_icon": loss.vehicle.country_made_icon.image_href,
                })

        serializer = LossSerializer(formatted_losses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
