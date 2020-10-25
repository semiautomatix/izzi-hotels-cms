from rest_framework import serializers

from . import models


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Rating
        fields = [
            "rating",
            "created",
            "last_updated",
            "review",
        ]

class ServiceBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ServiceBooking
        fields = [
            "created",
            "last_updated",
            "check_out_date_time",
            "end_date_time",
            "check_in_date_time",
            "start_date_time",
        ]

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Event
        fields = [
            "event_name",
            "last_updated",
            "end_date_time",
            "created",
            "event_metadata",
            "user",
            "start_date_time",
        ]
