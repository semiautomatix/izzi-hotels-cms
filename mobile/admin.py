from django.contrib import admin
from django import forms

from . import models


class RatingAdminForm(forms.ModelForm):

    class Meta:
        model = models.Rating
        fields = "__all__"


class RatingAdmin(admin.ModelAdmin):
    form = RatingAdminForm
    list_display = [
        "rating",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]


class ServiceBookingAdminForm(forms.ModelForm):

    class Meta:
        model = models.ServiceBooking
        fields = "__all__"


class ServiceBookingAdmin(admin.ModelAdmin):
    form = ServiceBookingAdminForm
    list_display = [
        "created",
        "last_updated",
        "check_out_date_time",
        "end_date_time",
        "check_in_date_time",
        "start_date_time",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]


class EventAdminForm(forms.ModelForm):

    class Meta:
        model = models.Event
        fields = "__all__"


class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_display = [
        "user",
        "event_name",
        "start_date_time",
        "end_date_time",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "created",
        "last_updated",
        "event_metadata",
    ]


admin.site.register(models.Rating, RatingAdmin)
admin.site.register(models.ServiceBooking, ServiceBookingAdmin)
admin.site.register(models.Event, EventAdmin)
