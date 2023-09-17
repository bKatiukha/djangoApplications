from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from src.oryx_equipment_losses.models import VehicleCategory, Vehicle, CountryMadeIcon, Loss, Report, SIDES
from src.oryx_equipment_losses.services.oryx_parser_service import parse_remote_oryx_page


def create_vehicle_category_if_not_exist(loss_vehicle_category_name, existing_categories):
    # Check if the category name exists in the existing_categories
    for category in existing_categories:
        if category.name == loss_vehicle_category_name:
            return category

    # If it doesn't exist, create a new VehicleCategory object
    category = VehicleCategory(name=loss_vehicle_category_name)
    category.save()
    existing_categories.add(category)
    return category


def create_county_made_icon_if_not_exist(loss_country_made_icon_href, existing_country_made_icons):
    # Check if the county_made_icon exists in the existing_country_made_icons
    for country_made_icon in existing_country_made_icons:
        if country_made_icon.image_href == loss_country_made_icon_href:
            return country_made_icon

    # If it doesn't exist, create a new CountryMadeIcon object
    country_made_icon = CountryMadeIcon(image_href=loss_country_made_icon_href)
    country_made_icon.save()
    existing_country_made_icons.add(country_made_icon)
    return country_made_icon


def create_vehicle_if_not_exist(
        loss_item,
        existing_vehicles,
        existing_country_made_icons,
        existing_categories
):
    vehicle_name = loss_item.get("vehicle_name")
    # Check if the vehicle_name exists in the existing_vehicles
    for vehicle in existing_vehicles:
        if vehicle.name == vehicle_name:
            return vehicle

    # If it doesn't exist, create a new Vehicle object
    vehicle_category = create_vehicle_category_if_not_exist(
        loss_item.get("vehicle_category_name"),
        existing_categories
    )
    country_made_icon = create_county_made_icon_if_not_exist(
        loss_item.get("vehicle_country_made_icon"),
        existing_country_made_icons
    )
    vehicle = Vehicle(
        name=vehicle_name,
        country_made_icon=country_made_icon,
        vehicle_category=vehicle_category
    )
    vehicle.save()
    existing_vehicles.add(vehicle)
    return vehicle


def create_loss_if_not_exist(
        loss_item,
        report,
        existing_losses,
        existing_vehicles,
        existing_country_made_icons,
        existing_categories
):
    name = loss_item.get("name")
    href = loss_item.get("href")
    side = loss_item.get("side")

    # Check if the name exists in the existing_losses
    for loss in existing_losses:
        if loss.href == href:
            return existing_losses

    # If it doesn't exist, create a new Loss object
    vehicle = create_vehicle_if_not_exist(
        loss_item,
        existing_vehicles,
        existing_country_made_icons,
        existing_categories
    )
    loss = Loss(
        name=name,
        href=href,
        side=side,
        vehicle=vehicle,
        report=report
    )
    loss.save()
    existing_losses.add(loss)
    return existing_losses


def create_report_if_not_exist():
    current_date = (timezone.now() + timezone.timedelta(hours=3)).date()

    try:
        # Try to retrieve a report with the current date
        report = Report.objects.get(report_date=current_date)
    except Report.DoesNotExist:
        # If no report with the current date exists, create a new one
        report = Report(report_date=current_date)
        report.save()

    return report


def save_parsed_data_to_bd(parsed_data, existed_report=None):
    # Retrieve all existing categories from the database
    existing_categories = set(VehicleCategory.objects.all())
    # Retrieve all existing country_made_icons from the database
    existing_country_made_icons = set(CountryMadeIcon.objects.all())
    # Retrieve all existing vehicles from the database
    existing_vehicles = set(Vehicle.objects.all())
    # Retrieve all existing losses from the database
    existing_losses = set(Loss.objects.all())
    # get current date report
    report = existed_report if existed_report else create_report_if_not_exist()

    for loss_item in parsed_data:
        create_loss_if_not_exist(
            loss_item,
            report,
            existing_losses,
            existing_vehicles,
            existing_country_made_icons,
            existing_categories
        )


@login_required
def oryx_equipment_losses(request):
    if request.method == 'POST':
        save_parsed_data_to_bd(
            parse_remote_oryx_page('UA') + parse_remote_oryx_page('RU'),
        )

    current_date = (timezone.now() + timezone.timedelta(hours=3)).date()
    current_date_report = Report.objects.filter(report_date=current_date)

    print('current_date_report', current_date, not current_date_report)
    if not current_date_report:
        print('not current_date_report', not current_date_report)
        save_parsed_data_to_bd(
            parse_remote_oryx_page('UA') + parse_remote_oryx_page('RU'),
            current_date_report
        )

    reports = Report.objects.prefetch_related(
        'report_losses',
        'report_losses__vehicle__vehicle_category',
        'report_losses__vehicle__country_made_icon'
    ).all()

    # Create a dictionary to store losses grouped by report date, side, category, and vehicle
    grouped_losses = {}

    for report in reports:
        report_date = report.report_date

        # loop for add empty reports in report_date for all sides
        for side, _ in SIDES:
            if side not in grouped_losses:
                grouped_losses[side] = {}
            if report_date not in grouped_losses[side]:
                grouped_losses[side][report_date] = {}

        for loss in report.report_losses.all():
            side = loss.side
            category = loss.vehicle.vehicle_category
            vehicle = loss.vehicle

            if category not in grouped_losses[side][report_date]:
                grouped_losses[side][report_date][category] = {}

            if vehicle not in grouped_losses[side][report_date][category]:
                grouped_losses[side][report_date][category][vehicle] = []

            grouped_losses[side][report_date][category][vehicle].append(loss)

    context = {
        'title': 'oryx_equipment_losses',
        'reports': reports,
        'grouped_losses': grouped_losses
    }
    return render(request, 'oryx_equipment_losses/reports.html', context=context)
