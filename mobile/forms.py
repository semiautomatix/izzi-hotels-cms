from django import forms
from . import models


class RatingForm(forms.ModelForm):
    class Meta:
        model = models.Rating
        fields = [
            "rating",
            "review",
        ]


class ServiceBookingForm(forms.ModelForm):
    class Meta:
        model = models.ServiceBooking
        fields = [
            "check_out_date_time",
            "end_date_time",
            "check_in_date_time",
            "start_date_time",
            "service",
            "user",
        ]


class EventForm(forms.ModelForm):
    class Meta:
        model = models.Event
        fields = [
            "event_name",
            "end_date_time",
            "event_metadata",
            "user",
            "start_date_time",
        ]
