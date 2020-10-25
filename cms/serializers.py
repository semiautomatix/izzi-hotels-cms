from rest_framework import serializers

from . import models


class HotelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Hotel
        fields = [
            "id",
            "created",
            "longitude",
            "latitude",
            "postal_code",
            "country",
            "city",
            "hotel_name",
            "last_updated",
            "address",
            "logo",
        ]

class HotelGroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.HotelGroup
        fields = [
            "logo",
            "head_office_postal_code",
            "head_office_country",
            "hotel_group_name",
            "head_office_address",
            "head_office_city",
            "last_updated",
            "head_office_latitude",
            "head_office_longitude",
            "created",
        ]

class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Room
        fields = [
            "id",
            "room_number",
            "last_updated",
            "created",
        ]

class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Booking
        fields = [
            "end_date",
            "adults",
            "start_date",
            "booking_status",
            "created",
            "children",
            "last_updated",
        ]


class BookingTrendSerializer(serializers.ModelSerializer):
    hotel_group__hotel_group_name = serializers.StringRelatedField(many=False)
    hotel__hotel_name = serializers.StringRelatedField(many=False)
    total = serializers.IntegerField(
        read_only=True
    )
    
    class Meta:
        model = models.Booking
        fields = [
            "hotel_group__hotel_group_name", 
            "hotel_group_id", 
            "hotel__hotel_name", 
            "hotel_id", 
            "total"
        ]


class ServiceBookingSerializer(serializers.ModelSerializer):
    service__hotel_group__hotel_group_name = serializers.StringRelatedField(many=False)
    service__hotel_group_id = serializers.IntegerField(
        read_only=True
    )
    service__hotel__hotel_name = serializers.StringRelatedField(many=False)
    service__hotel_id = serializers.IntegerField(
        read_only=True
    )
    total = serializers.IntegerField(
        read_only=True
    )
    
    class Meta:
        model = models.Booking
        fields = [
            "service__service_category_id",
            "service__service_name",
            "service__service_category__category_name",
            "service__service_category_id",
            "service__hotel_group__hotel_group_name", 
            "service__hotel_group_id", 
            "service__hotel__hotel_name", 
            "service__hotel_id", 
            "total"
        ]


class IconSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Icon
        fields = [
            "image",
            "created",
            "last_updated",
            "icon_name",
        ]

class ServiceCategorySerializer(serializers.ModelSerializer):
    service__hotel_group__hotel_group_name = serializers.StringRelatedField(many=False)
    service__hotel_group_id = serializers.IntegerField(
        read_only=True
    )
    service__hotel__hotel_name = serializers.StringRelatedField(many=False)
    service__hotel_id = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = models.Service
        fields = [
            "category_name",
            "service__hotel_group__hotel_group_name", 
            "service__hotel_group_id", 
            "service__hotel__hotel_name", 
            "service__hotel_id",
            "created",
            "last_updated"
        ]


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Service
        fields = [
            "service_name",
            "meeting_room",
            "created",
            "type",
            "last_updated",
            "rate",
        ]

class HotelGallerySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.HotelGallery
        fields = [
            "created",
            "image",
            "last_updated",
        ]


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.File
        fields = "__all__"