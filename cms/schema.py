# cookbook/ingredients/schema.py
import graphene
from django.db.models import Q
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from cms.models import HotelGroup, Hotel, HotelGallery, Booking, Room, Icon, Service
from datetime import datetime

import logging

# Get an instance of a logger
logger = logging.getLogger('django')

# enums
class BookingStatuses(graphene.Enum):
    CANCELLED = 0
    CONFIRMED = 1
    CHECKED_IN = 2
    CHECKED_OUT = 3

class ServiceTypes(graphene.Enum):
    SERVICE =  'service'
    CO_SHARE = 'co-share'
    MEETING_ROOM = 'meeting_room'    

    '''@property
    def description(self):
        if self == ServiceTypes.SERVICE:
            return 'Service'
        if self == ServiceTypes.CO_SHARE:
            return 'Co-share'
        if self == ServiceTypes.MEETING_ROOM:
            return 'Meeting Room'            
    '''

class HotelGroupType(DjangoObjectType):
    class Meta:
        model = HotelGroup


class HotelType(DjangoObjectType):
    class Meta:
        model = Hotel


class HotelGalleryType(DjangoObjectType):
    class Meta:
        model = HotelGallery


class BookingType(DjangoObjectType):
    class Meta:
        model = Booking


class RoomType(DjangoObjectType):
    class Meta:
        model = Room


class IconType(DjangoObjectType):
    class Meta:
        model = Icon


class ServiceType(DjangoObjectType):
    class Meta:
        model = Service


class Query(object):
    all_hotelgroups = graphene.List(HotelGroupType)

    hotel = graphene.Field(HotelType,
                           id=graphene.Int())    
    all_hotels = graphene.List(HotelType)
    all_hotelgalleries = graphene.List(HotelGalleryType)
    random_hotel = graphene.Field(HotelType) 
    hotel_search = graphene.List(HotelType,
                                 search_string=graphene.String(),
                                 latitude=graphene.Float(required=False),
                                 longitude=graphene.Float(required=False))

    booking = graphene.Field(BookingType,
                             id=graphene.Int())   
    bookings = graphene.List(BookingType,
                             current_user=graphene.Boolean(),
                             user_id=graphene.Int(required=False),
                             start_date=graphene.Date(required=False),
                             end_date=graphene.Date(required=False),
                             booking_status=BookingStatuses(required=False))
    all_bookings = graphene.List(BookingType)

    room = graphene.Field(RoomType,
                          id=graphene.Int())                           
    all_rooms = graphene.List(RoomType)
    all_icons = graphene.List(IconType)

    service = graphene.Field(ServiceType,
                             id=graphene.Int())        
    all_services = graphene.List(ServiceType)

    def resolve_all_hotelgroups(self, info, **kwargs):
        return HotelGroup.objects.all()

    def resolve_all_hotels(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Hotel.objects.all()

    def resolve_all_hotelgalleries(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return HotelGallery.objects.all()

    def resolve_all_bookings(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Booking.objects.all()

    def resolve_all_rooms(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Room.objects.all()

    def resolve_all_icons(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Icon.objects.all()                                        
        
    def resolve_all_services(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Service.objects.all()

    def resolve_hotel(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Hotel.objects.get(pk=id)

        return None        

    def resolve_random_hotel(self, info, **kwargs):
        # random order and select the first record
        return Hotel.objects.order_by("?").first() 

    def resolve_hotel_search(self, info, **kwargs):
        latitude = kwargs.get('latitude') 
        longitude = kwargs.get('longitude') 
        search_string = kwargs.get('search_string') 

        return Hotel.objects.filter(Q(hotel_name__icontains=search_string) | Q(city__icontains=search_string))

    def resolve_booking(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Booking.objects.get(pk=id)

        return None       

    def resolve_bookings(self, info, **kwargs):
        current_user = kwargs.get('current_user')
        user_id = kwargs.get('user_id')
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        booking_status = kwargs.get('booking_status')

        qs = Booking.objects.all()

        if current_user is not None and current_user:
            user = info.context.user
            qs = qs.filter(user_id=user.id)
        elif user_id is not None:
            qs = qs.filter(user_id=user_id)            
        #if start_date is not None:
        #    qs = qs.filter(start_date__gte=start_date)
        if end_date is not None:
            qs = qs.filter(end_date__lte=end_date)
        if booking_status is not None:
            qs = qs.filter(booking_status=booking_status)            

        return qs;                

    def resolve_room(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Room.objects.get(pk=id)

        return None   

    def resolve_service(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Service.objects.get(pk=id)

        return None   


# Create Input Object Types 
class BookingInput(graphene.InputObjectType):
    id = graphene.ID()
    hotel_id = graphene.Int(required=True)
    start_date = graphene.DateTime(required=True)
    end_date = graphene.DateTime(required=True)
    adults = graphene.Int(default_value=1)
    children = graphene.Int(default_value=0)
    rooms = graphene.Int(default_value=1)
    # booking_status = graphene.Enum('Status', [('Confirmed', 1), ('Cancelled', 2)])


# Create mutations for ratings
class CreateBooking(graphene.Mutation):
    class Arguments:
        input = BookingInput(required=True)

    ok = graphene.Boolean()
    booking = graphene.Field(BookingType)

    @staticmethod
    @login_required
    # @permission_required('auth.change_user')
    def mutate(root, info, input=None):
        user = info.context.user
        ok = True
        hotel = Hotel.objects.get(pk=input.hotel_id)
        logger.info(hotel)
        booking_instance = Booking(
            user_id=user.id, # this must come from the token
            hotel_id=input.hotel_id,
            hotel_group_id=hotel.hotel_group_id,
            start_date=input.start_date,
            end_date=input.end_date,
            adults=input.adults,
            children=input.children,
            rooms=input.rooms,
            booking_status=1 # Confirmed
        )
        booking_instance.save()
        return CreateBooking(ok=ok, booking=booking_instance)

'''
class CancelBooking(graphene.Mutation):
    class Arguments:
        booking_id = graphene.ID(required=True)

    ok = graphene.Boolean()
    booking = graphene.Field(BookingType)

    @staticmethod
    @login_required
    # @permission_required('auth.change_user')
    def mutate(root, info, booking_id):
        ok = False
        booking_instance = Booking.objects.get(pk=booking_id)
        if booking_instance:
            ok = True
            booking_instance.booking_status = 2 # Cancelled
            booking_instance.save()
            return CancelBooking(ok=ok, booking=booking_instance)        
        return CancelBooking(ok=ok, booking=None) 
'''

class CheckInBooking(graphene.Mutation):
    class Arguments:
        booking_id = graphene.ID(required=True)

    ok = graphene.Boolean()
    booking = graphene.Field(BookingType)

    @staticmethod
    @login_required
    # @permission_required('auth.change_user')
    def mutate(root, info, booking_id):
        ok = False
        booking_instance = Booking.objects.get(pk=booking_id)
        if booking_instance:
            ok = True
            booking_instance.booking_status = 2 # Checked In
            booking_instance.check_in_date_time = datetime.now()
            booking_instance.save()
            return CheckInBooking(ok=ok, booking=booking_instance)        
        return CheckInBooking(ok=ok, booking=None) 

class CheckOutBooking(graphene.Mutation):
    class Arguments:
        booking_id = graphene.ID(required=True)

    ok = graphene.Boolean()
    booking = graphene.Field(BookingType)

    @staticmethod
    @login_required
    # @permission_required('auth.change_user')
    def mutate(root, info, booking_id):
        ok = False
        booking_instance = Booking.objects.get(pk=booking_id)
        if booking_instance:
            ok = True
            booking_instance.booking_status = 3 # Checked Out
            booking_instance.check_out_date_time = datetime.now()
            booking_instance.save()
            return CheckOutBooking(ok=ok, booking=booking_instance)        
        return CheckOutBooking(ok=ok, booking=None)                 


class Mutation(graphene.ObjectType):
    create_booking = CreateBooking.Field() 
    # cancel_booking = CancelBooking.Field()       
    check_in_booking = CheckInBooking.Field()       
    check_out_booking = CheckOutBooking.Field()       
                
