from django.utils import timezone

from src.oryx_equipment_losses.models import Report


def get_all_reports():
    return Report.objects.prefetch_related(
        'report_losses',
        'report_losses__vehicle__vehicle_category',
        'report_losses__vehicle__country_made_icon'
    ).all()


def is_need_update(reports) -> bool:
    current_date = timezone.now().date()
    return not [report for report in reports if report.report_date == current_date]
