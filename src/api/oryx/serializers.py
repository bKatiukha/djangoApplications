from rest_framework import serializers


class LossSerializer(serializers.Serializer):
    name = serializers.CharField()
    side = serializers.CharField()
    category = serializers.CharField()
    vehicle = serializers.CharField()
    country_made_icon = serializers.CharField()
    report_date = serializers.DateField()


class GroupedLossesSerializer(serializers.Serializer):
    side = serializers.CharField()
    report_date = serializers.DateField()
    category = serializers.CharField()
    vehicle = serializers.CharField()
    losses = serializers.ListField(child=LossSerializer())
