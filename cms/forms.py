from django import forms
from . import models
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger('django')

class HotelForm(forms.ModelForm):
    class Meta:
        model = models.Hotel
        fields = [
            "latitude",
            "longitude",
            "postal_code",
            "country",
            "city",
            "hotel_name",
            "address",
            "logo",
            "hotel_group",
            "ibe_domain",
            "ibe_id"
        ]


class RoomForm(forms.ModelForm):
    class Meta:
        model = models.Room
        fields = [
            "room_number",
            "hotel",
        ]


class BookingForm(forms.ModelForm):
    class Meta:
        model = models.Booking
        fields = [
            "end_date",
            "adults",
            "start_date",
            "booking_status",
            "children",
            "hotel",
            "hotel_group",
            "user",
            "room",
        ]


class IconForm(forms.ModelForm):
    class Meta:
        model = models.Icon
        fields = [
            "image",
            "icon_name",
        ]


class ServiceForm(forms.ModelForm):
    class Meta:
        model = models.Service
        fields = [
            "service_name",
            "meeting_room",
            "service_type",
            "location",
            "rate",
            "hotel",
            "hotel_group",
            "icon",
        ]


class HotelGroupForm(forms.ModelForm):
    class Meta:
        model = models.HotelGroup
        fields = [
            "logo",
            "head_office_postal_code",
            "head_office_country",
            "hotel_group_name",
            "head_office_address",
            "head_office_city",
            "head_office_latitude",
            "head_office_longitude",
        ]


class HotelGalleryForm(forms.ModelForm):
    class Meta:
        model = models.HotelGallery
        fields = [
            "image",
            "hotel",
        ]

