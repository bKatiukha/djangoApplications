from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from src.oryx_equipment_losses.models import Loss, Report
from src.oryx_equipment_losses.utils.oryx_data_processor import OryxDataProcessor
from src.oryx_equipment_losses.utils.oryx_scraper import OryxScraper
from src.oryx_equipment_losses.utils.oryx_utils import get_all_reports, is_need_update


# Create a dictionary to store losses grouped by report date, side, category, and vehicle
def group_losses_for_display(reports):
    grouped_losses = {}

    for report in reports:
        report_date = report.report_date
        for loss in report.report_losses.all():
            side = loss.side
            category = loss.vehicle.vehicle_category
            vehicle = loss.vehicle
            grouped_losses \
                .setdefault(side, {}) \
                .setdefault(report_date, {}) \
                .setdefault(category, {}) \
                .setdefault(vehicle, [])
            # Append the loss to the list
            grouped_losses[side][report_date][category][vehicle].append(loss)

    # sort grouped_losses by key (always display sides in same order)
    grouped_losses = {key: grouped_losses[key] for key in sorted(grouped_losses.keys(), reverse=True)}
    return grouped_losses


def format_looses_for_statistic(reports):
    formatted_losses = []
    for report in reports:
        for loss in report.report_losses.all():
            formatted_losses.append({
                "name": loss.name,
                "side": loss.side,
                "category": loss.vehicle.vehicle_category.name,
                "vehicle": loss.vehicle.name,
                "date_added": str(report.report_date)
            })
    return formatted_losses


@login_required
def oryx_equipment_losses(request):
    reports = get_all_reports()
    print('losses length', Loss.objects.count())

    if is_need_update(reports):
        scraper = OryxScraper()
        data_processor = OryxDataProcessor()
        data_processor.save_parsed_data_to_db((scraper.scrape_oryx_sides()))

    context = {
        'title': 'oryx_equipment_losses',
        'grouped_losses': group_losses_for_display(reports),
    }
    return render(request, 'oryx_equipment_losses/reports.html', context=context)


@login_required
def oryx_losses_statistics(request):
    reports = get_all_reports()
    context = {
        'title': 'oryx losses statistics',
        'formatted_losses': format_looses_for_statistic(reports)
    }
    return render(request, 'oryx_equipment_losses/statistics.html', context=context)


@login_required
def force_update_oryx_losses(request):
    if request.method == 'POST':
        scraper = OryxScraper()
        data_processor = OryxDataProcessor()
        data_processor.save_parsed_data_to_db((scraper.scrape_oryx_sides()))

    return redirect('oryx_equipment_losses')
