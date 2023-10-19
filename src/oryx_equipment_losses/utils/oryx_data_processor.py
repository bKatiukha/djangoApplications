from django.utils import timezone
from typing import List
from src.oryx_equipment_losses.models import Report, VehicleCategory, CountryMadeIcon, Vehicle, Loss
from django.db import IntegrityError


class OryxDataProcessor:
    def __init__(self):
        self.report = self._get_or_create_report()
        self.existing_categories = {category.name: category for category in VehicleCategory.objects.all()}
        self.existing_country_made_icons = {icon.image_href: icon for icon in CountryMadeIcon.objects.all()}
        self.existing_vehicles = {
            (vehicle.name, vehicle.country_made_icon.image_href): vehicle
            for vehicle in Vehicle.objects.all()
        }
        self.existing_losses = {
            (loss.name, loss.side, loss.vehicle.name): loss
            for loss in Loss.objects.select_related('vehicle').all()
        }

    # Public methods
    def save_parsed_data_to_db(self, parsed_data: List[dict]):
        print('parsed_data length', len(parsed_data))
        for loss_item in parsed_data:
            self._get_or_create_loss(loss_item)

    # Private methods
    def _get_or_create_category(self, name: str) -> VehicleCategory:
        if name in self.existing_categories:
            return self.existing_categories[name]
        else:
            new_category = CountryMadeIcon.objects.create(name=name)
            self.existing_categories[name] = new_category
            return new_category

    def _get_or_create_country_made_icon(self, image_href: str) -> CountryMadeIcon:
        if image_href in self.existing_country_made_icons:
            return self.existing_country_made_icons[image_href]
        else:
            new_icon = CountryMadeIcon.objects.create(image_href=image_href)
            self.existing_country_made_icons[image_href] = new_icon
            return new_icon

    def _get_or_create_vehicle(self, loss_item: dict) -> Vehicle:
        name = loss_item["vehicle_name"]
        icon_href = loss_item["vehicle_country_made_icon"]
        key = (name, icon_href)

        if key in self.existing_vehicles:
            return self.existing_vehicles[key]
        else:
            new_vehicle = Vehicle.objects.create(
                name=name,
                country_made_icon=self._get_or_create_country_made_icon(icon_href),
                vehicle_category=self._get_or_create_category(loss_item["vehicle_category_name"])
            )
            self.existing_vehicles[key] = new_vehicle
            return new_vehicle

    def _get_or_create_loss(self, loss_item: dict):
        name = loss_item["name"]
        href = loss_item["href"]
        side = loss_item["side"]
        vehicle_name = loss_item["vehicle_name"]
        key = (name, side, vehicle_name)
        existing_loss = self.existing_losses.get(key)

        if existing_loss:
            if existing_loss.href != href:
                try:
                    existing_loss.href = href
                    existing_loss.save()
                except IntegrityError:
                    print(f"Error: Can't update Loss href for {name}, {vehicle_name}, {side}. "
                          f"It would cause duplication.")
            return existing_loss
        else:
            vehicle = self._get_or_create_vehicle(loss_item)
            loss = Loss.objects.create(
                name=name,
                href=href,
                side=side,
                vehicle=vehicle,
                report=self.report
            )
            self.existing_losses[key] = loss

    def _get_or_create_report(self) -> Report:
        current_date = timezone.now().date()

        try:
            return Report.objects.get(report_date=current_date)
        except Report.DoesNotExist:
            return Report.objects.create(report_date=current_date)
