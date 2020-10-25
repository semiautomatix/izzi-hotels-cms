from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.db.models import Count

from . import serializers
from . import models
from mobile.models import ServiceBooking
from users.models import UserMetadata

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger('django')


class HotelViewSet(viewsets.ModelViewSet):
    """ViewSet for the Hotel class"""

    queryset = models.Hotel.objects.all()
    serializer_class = serializers.HotelSerializer
    permission_classes = [permissions.IsAuthenticated]
    # extend definitiont to include filtering by
    #   hotel_group_id
    def list(self, request, pk=None):
        if 'hotel_group_id' in request.GET:
            queryset = models.Hotel.objects.all().filter(hotel_group_id=request.GET["hotel_group_id"])
            serializer = serializers.HotelSerializer(queryset, many=True)
            return Response(serializer.data)
        queryset = models.Hotel.objects.all()
        serializer = serializers.HotelSerializer(queryset, many=True)
        return Response(serializer.data)


class RoomViewSet(viewsets.ModelViewSet):
    """ViewSet for the Room class"""

    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    # extend definitiont to include filtering by
    #   hotel_id
    def list(self, request, pk=None):
        if 'hotel_id' in request.GET:
            queryset = models.Room.objects.all().filter(hotel_id=request.GET["hotel_id"])
            serializer = serializers.RoomSerializer(queryset, many=True)
            return Response(serializer.data)
        queryset = models.Hotel.objects.all()
        serializer = serializers.RoomSerializer(queryset, many=True)
        return Response(serializer.data)    


class BookingViewSet(viewsets.ModelViewSet):
    """ViewSet for the Booking class"""

    queryset = models.Booking.objects.all()
    serializer_class = serializers.BookingSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookingTrendViewSet(viewsets.ViewSet):
    """ViewSet for the Booking class"""

    def list(self, request):
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        hotel_group_id = request.query_params.get('hotel_group_id', None)

        current_user = request.user
        user_id = current_user.pk
        user_metadata = UserMetadata.objects.get(user_id=user_id)        

        bookings = None
        
        # if group or hotel then apply filter
        if current_user.groups.filter(name='Hotel Group Administrators').exists(): 
            hotel_group_id = user_metadata.hotel_group_id
            bookings = models.Booking.objects.filter(hotel_group_id=hotel_group_id).filter(booking_status=1)\
                .values('hotel__hotel_name', 'hotel_id', 'hotel__city') \
                .annotate(total=Count('id')) 
        elif current_user.groups.filter(name='Hotel Administrators').exists(): 
            hotel_id = user_metadata.hotel_id
            bookings = models.Booking.objects.filter(hotel_id=hotel_id).filter(booking_status=1)\
                .values('hotel__hotel_name', 'hotel_id', 'hotel__city') \
                .annotate(total=Count('id')) 
        else:
            bookings = models.Booking.objects.filter(booking_status=1)\
                .values('hotel_group__hotel_group_name', 'hotel_group_id', 'hotel__hotel_name', 'hotel_id', 'hotel__city') \
                .annotate(total=Count('id')) 

        # if end_date and start_date:
        #    bookings = bookings.filter(start_date__gte=start_date).filter(end_date__lte=end_date)

        if hotel_group_id: 
            bookings = bookings.filter(hotel_group_id=hotel_group_id)

        serializer = serializers.BookingTrendSerializer(bookings, many=True)
        return Response(serializer.data)

    permission_classes = [permissions.IsAuthenticated]


class IconViewSet(viewsets.ModelViewSet):
    """ViewSet for the Icon class"""

    queryset = models.Icon.objects.all()
    serializer_class = serializers.IconSerializer
    permission_classes = [permissions.IsAuthenticated]


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for the Service class"""

    queryset = models.ServiceCategory.objects.all()
    serializer_class = serializers.ServiceCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class ServiceViewSet(viewsets.ModelViewSet):
    """ViewSet for the Service class"""

    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]


class HotelGroupViewSet(viewsets.ModelViewSet):
    """ViewSet for the HotelGroup class"""

    queryset = models.HotelGroup.objects.all()
    serializer_class = serializers.HotelGroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class HotelGalleryViewSet(viewsets.ModelViewSet):
    """ViewSet for the HotelGallery class"""

    queryset = models.HotelGallery.objects.all()
    serializer_class = serializers.HotelGallerySerializer
    permission_classes = [permissions.IsAuthenticated]


class CoShareBookingViewSet(viewsets.ViewSet):
    """ViewSet for the Booking class"""

    def list(self, request):
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        hotel_group_id = request.query_params.get('hotel_group_id', None)

        current_user = request.user
        user_id = current_user.pk
        user_metadata = UserMetadata.objects.get(user_id=user_id)        

        bookings = None
        
        # if group or hotel then apply filter
        if current_user.groups.filter(name='Hotel Group Administrators').exists(): 
            hotel_group_id = user_metadata.hotel_group_id
            bookings = ServiceBooking.objects.filter(service__service_type='co_share')\
                .filter(service__hotel_group_id=hotel_group_id)\
                .values('service__hotel__hotel_name', 'service__hotel_id') \
                .annotate(total=Count('id')) 
        elif current_user.groups.filter(name='Hotel Administrators').exists(): 
            hotel_id = user_metadata.hotel_id
            bookings = ServiceBooking.objects.filter(service__service_type='co_share')\
                .filter(service__hotel_id=hotel_id)\
                .values('service__hotel__hotel_name', 'service__hotel_id') \
                .annotate(total=Count('id')) 
        else:
            bookings = ServiceBooking.objects.filter(service__service_type='co_share')\
                .values('service__hotel_group__hotel_group_name', 'service__hotel_group_id', 'service__hotel__hotel_name', 'service__hotel_id')\
                .annotate(total=Count('id')) 

        if end_date and start_date:
            bookings = bookings.filter(start_date_time__gte=start_date).filter(end_date_time__lte=end_date)

        # if hotel_group_id: 
        #    bookings = bookings.filter(hotel_group_id=hotel_group_id)

        serializer = serializers.ServiceBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    permission_classes = [permissions.IsAuthenticated]


class MeetingRoomBookingViewSet(viewsets.ViewSet):
    """ViewSet for the Booking class"""

    def list(self, request):
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        hotel_group_id = request.query_params.get('hotel_group_id', None)

        current_user = request.user
        user_id = current_user.pk
        user_metadata = UserMetadata.objects.get(user_id=user_id)        

        bookings = None
        
        # if group or hotel then apply filter
        if current_user.groups.filter(name='Hotel Group Administrators').exists(): 
            hotel_group_id = user_metadata.hotel_group_id
            bookings = ServiceBooking.objects.filter(service__service_type='meeting_room')\
                .filter(service__hotel_group_id=hotel_group_id)\
                .values('service__hotel__hotel_name', 'service__hotel_id') \
                .annotate(total=Count('id')) 
        elif current_user.groups.filter(name='Hotel Administrators').exists(): 
            hotel_id = user_metadata.hotel_id
            bookings = ServiceBooking.objects.filter(service__service_type='meeting_room')\
                .filter(service__hotel_id=hotel_id)\
                .values('service__hotel__hotel_name', 'service__hotel_id') \
                .annotate(total=Count('id')) 
        else:
            bookings = ServiceBooking.objects.filter(service__service_type='meeting_room')\
                .values('service__hotel_group__hotel_group_name', 'service__hotel_group_id', 'service__hotel__hotel_name', 'service__hotel_id')\
                .annotate(total=Count('id')) 

        if end_date and start_date:
            bookings = bookings.filter(start_date_time__gte=start_date).filter(end_date_time__lte=end_date)

        # if hotel_group_id: 
        #    bookings = bookings.filter(hotel_group_id=hotel_group_id)

        serializer = serializers.ServiceBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    permission_classes = [permissions.IsAuthenticated]

class ServiceBookingViewSet(viewsets.ViewSet):
    """ViewSet for the Booking class"""

    def list(self, request):
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        hotel_group_id = request.query_params.get('hotel_group_id', None)

        current_user = request.user
        user_id = current_user.pk
        user_metadata = UserMetadata.objects.get(user_id=user_id)        

        bookings = None
        
        # if group or hotel then apply filter
        if current_user.groups.filter(name='Hotel Group Administrators').exists(): 
            hotel_group_id = user_metadata.hotel_group_id
            bookings = ServiceBooking.objects\
                .filter(service__hotel_group_id=hotel_group_id)\
                .values('service__hotel__hotel_name', 'service__hotel_id') \
                .annotate(total=Count('id')) 
        elif current_user.groups.filter(name='Hotel Administrators').exists(): 
            hotel_id = user_metadata.hotel_id
            bookings = ServiceBooking.objects\
                .filter(service__hotel_id=hotel_id)\
                .values('service__hotel__hotel_name', 'service__hotel_id') \
                .annotate(total=Count('id')) 
        else:
            bookings = ServiceBooking.objects\
                .values('service__hotel_group__hotel_group_name', 'service__hotel_group_id', 'service__hotel__hotel_name', 'service__hotel_id')\
                .annotate(total=Count('id')) 

        if end_date and start_date:
            bookings = bookings.filter(start_date_time__gte=start_date).filter(end_date_time__lte=end_date)

        # if hotel_group_id: 
        #    bookings = bookings.filter(hotel_group_id=hotel_group_id)

        serializer = serializers.ServiceBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    permission_classes = [permissions.IsAuthenticated]
