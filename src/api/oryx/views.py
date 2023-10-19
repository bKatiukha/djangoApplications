from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.oryx.serializers import LossSerializer
from src.oryx_equipment_losses.utils.oryx_data_processor import OryxDataProcessor
from src.oryx_equipment_losses.utils.oryx_scraper import OryxScraper
from src.oryx_equipment_losses.utils.oryx_utils import get_all_reports, is_need_update


class LossesStatisticsAPIView(APIView):
    def get(self, request):
        reports = get_all_reports()

        if is_need_update(reports):
            scraper = OryxScraper()
            data_processor = OryxDataProcessor()
            data_processor.save_parsed_data_to_db((scraper.scrape_oryx_sides()))

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
