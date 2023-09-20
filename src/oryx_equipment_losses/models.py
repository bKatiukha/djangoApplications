from django.db import models

SIDES = (
        ('UA', 'UA'),
        ('RU', 'RU'),
    )


class VehicleCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class CountryMadeIcon(models.Model):
    image_href = models.CharField(max_length=255, unique=True)


class Vehicle(models.Model):
    name = models.CharField(max_length=255)
    country_made_icon = models.ForeignKey(CountryMadeIcon, blank=True, default=None, on_delete=models.DO_NOTHING)
    vehicle_category = models.ForeignKey(VehicleCategory, blank=True, default=None, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'country_made_icon')


class Report(models.Model):
    report_date = models.DateField(auto_now_add=True, unique=True)

    class Meta:
        ordering = ('-report_date',)

    def __str__(self):
        return self.report_date


class Loss(models.Model):
    name = models.CharField(max_length=255)
    href = models.CharField(max_length=255)
    side = models.CharField(max_length=2, choices=SIDES)
    vehicle = models.ForeignKey(Vehicle, blank=True, default=None, on_delete=models.DO_NOTHING)
    report = models.ForeignKey(Report, blank=True, default=None,
                               related_name='report_losses', on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('name', 'href', 'vehicle')
