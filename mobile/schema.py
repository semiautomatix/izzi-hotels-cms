# cookbook/ingredients/schema.py
import graphene
import json
# logging
import logging
from django.conf import settings
from django.db.models import Q
from cms.models import Hotel
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphql import GraphQLError
from mobile.models import Rating, ServiceBooking, Event
from django.contrib.auth.models import User
from datetime import datetime
from cms.schema import ServiceTypes
# email
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site


# Get an instance of a logger
logger = logging.getLogger('django')


class RatingType(DjangoObjectType):
    class Meta:
        model = Rating


class ServiceBookingType(DjangoObjectType):
    class Meta:
        model = ServiceBooking


class EventType(DjangoObjectType):
    class Meta:
        model = Event


class Query(object):
    ratings = graphene.List(RatingType,                            
                            user_id=graphene.Int(),
                            hotel_id=graphene.Int())
    all_ratings = graphene.List(RatingType)
    
    service_bookings = graphene.List(ServiceBookingType,
                                     current_user=graphene.Boolean(),
                                     user_id=graphene.Int(),
                                     start_date_time=graphene.DateTime(),
                                     end_date_time=graphene.DateTime(),                                     
                                     service_type=ServiceTypes())
    all_service_bookings = graphene.List(ServiceBookingType)

    events = graphene.List(EventType,
                           user_id=graphene.Int(),
                           start_date_time=graphene.DateTime(),
                           end_date_time=graphene.DateTime())    
    all_events = graphene.List(EventType)

    @login_required
    def resolve_all_ratings(self, info, **kwargs):
        return Rating.objects.all()

    @login_required
    def resolve_all_servicebookings(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return ServiceBooking.objects.all()

    @login_required
    def resolve_all_events(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Event.objects.all()

    @login_required
    def resolve_ratings(self, info, **kwargs):
        user_id = kwargs.get('user_id')
        hotel_id = kwargs.get('hotel_id')

        qs = Rating.objects.all()
        
        if user_id is not None:
            qs = qs.filter(user_id=user_id) 
        if hotel_id is not None:
            qs = qs.filter(hotel_id=hotel_id)             

        return qs;   

    @login_required  
    def resolve_service_bookings(self, info, **kwargs):
        current_user = kwargs.get('current_user')
        user_id = kwargs.get('user_id')
        start_date_time = kwargs.get('start_date_time')
        end_date_time = kwargs.get('end_date_time')
        service_type = kwargs.get('service_type')

        qs = ServiceBooking.objects.all()
        
        if current_user is not None and current_user:
            user = info.context.user
            qs = qs.filter(user_id=user.id)
        elif user_id is not None:
            qs = qs.filter(user_id=user_id)
        if service_type is not None:
            qs = qs.filter(service__service_type=service_type)                
        #if start_date_time is not None:
        #    qs = qs.filter(start_date_time__gte=start_date_time)
        if end_date_time is not None:
            qs = qs.filter(end_date_time__lte=end_date_time)

        return qs;      

    @login_required  
    def resolve_events(self, info, **kwargs):
        user_id = kwargs.get('user_id')
        start_date_time = kwargs.get('start_date_time')
        end_date_time = kwargs.get('end_date_time')

        qs = Event.objects.all()
        
        if user_id is not None:
            qs = qs.filter(user_id=user_id)
        #if start_date_time is not None:
        #    qs = qs.filter(start_date_time__gte=start_date_time)
        if end_date_time is not None:
            qs = qs.filter(end_date_time__lte=end_date_time)

        return qs;             


# Create Input Object Types
class RatingInput(graphene.InputObjectType):
    id = graphene.ID()
    hotel_id = graphene.ID(required=True)
    rating = graphene.Int(required=True)
    review = graphene.String()
    # hotel_gallery = graphene.List(ActorInput)

class ServiceBookingInput(graphene.InputObjectType):
    id = graphene.ID()
    # hotel_id = graphene.ID(required=True)
    service_id = graphene.ID(required=True)
    start_date_time = graphene.DateTime(required=True)
    end_date_time = graphene.DateTime(required=True)
    # hotel_gallery = graphene.List(ActorInput)    

class EventInput(graphene.InputObjectType):
    id = graphene.ID()
    event_name = graphene.String(required=True)
    start_date_time = graphene.DateTime(required=True)
    end_date_time = graphene.DateTime(required=True)
    event_metadata = graphene.JSONString(required=True)

class SupportInput(graphene.InputObjectType):
    hotel_id = graphene.ID(required=True)
    subject = graphene.String(required=True)
    message = graphene.String(required=True)

# Create mutations for ratings
class CreateRating(graphene.Mutation):
    class Arguments:
        input = RatingInput(required=True)

    ok = graphene.Boolean()
    rating = graphene.Field(RatingType)

    @staticmethod
    @login_required
    # @permission_required('auth.change_user')
    def mutate(root, info, input=None):
        user = info.context.user
        ok = True
        rating_instance = Rating(
            user_id=user.id, # this must come from the token
            hotel_id=input.hotel_id,
            rating=input.rating,
            review=input.review
        )
        rating_instance.save()
        return CreateRating(ok=ok, rating=rating_instance)

# Create mutations for service bookings
class CreateServiceBooking(graphene.Mutation):
    class Arguments:
        input = ServiceBookingInput(required=True)

    ok = graphene.Boolean()
    service_booking = graphene.Field(ServiceBookingType)

    @staticmethod
    @login_required
    # @permission_required('auth.change_user')
    def mutate(root, info, input=None):
        user = info.context.user
        ok = False
        # if a meeting need to check there is not an existing booking
        bookings = ServiceBooking.objects.filter(
            Q(service_id=input.service_id, start_date_time__gte=input.start_date_time, start_date_time__lte=input.end_date_time) |\
            Q(service_id=input.service_id, end_date_time__gte=input.start_date_time, end_date_time__lte=input.end_date_time))         

        if bookings.count() != 0:
            raise GraphQLError('Booking already exists at this time for this booking')
        else:
            ok=True         
            service_booking_instance = ServiceBooking(
                user_id=user.id, # this must come from the token
                service_id = input.service_id,
                start_date_time = input.start_date_time,
                end_date_time = input.end_date_time
            )
            service_booking_instance.save()
            return CreateServiceBooking(ok=ok, service_booking=service_booking_instance)      


class CancelServiceBooking(graphene.Mutation):
    class Arguments:
        service_booking_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @staticmethod
    @login_required
    # @permission_required('auth.change_user')
    def mutate(root, info, service_booking_id):
        ok = False
        service_booking_instance = ServiceBooking.objects.get(pk=service_booking_id)
        if service_booking_instance:
            ok = True
            service_booking_instance.delete()
            return CancelServiceBooking(ok=ok)        
        return CancelServiceBooking(ok=ok) 

class CheckInServiceBooking(graphene.Mutation):
    class Arguments:
        service_booking_id = graphene.ID(required=True)

    ok = graphene.Boolean()
    service_booking = graphene.Field(ServiceBookingType)

    @staticmethod
    @login_required
    # @permission_required('auth.change_user')
    def mutate(root, info, service_booking_id):
        ok = False
        service_booking_instance = ServiceBooking.objects.get(pk=service_booking_id)
        if service_booking_instance:
            ok = True
            service_booking_instance.check_in_date_time = datetime.now()
            service_booking_instance.save()
            return CheckInServiceBooking(ok=ok, service_booking=service_booking_instance)        
        return CheckInServiceBooking(ok=ok, service_booking=None) 

class CheckOutServiceBooking(graphene.Mutation):
    class Arguments:
        service_booking_id = graphene.ID(required=True)

    ok = graphene.Boolean()
    service_booking = graphene.Field(ServiceBookingType)

    @staticmethod
    @login_required
    # @permission_required('auth.change_user')
    def mutate(root, info, service_booking_id):
        ok = False
        service_booking_instance = ServiceBooking.objects.get(pk=service_booking_id)
        if service_booking_instance:
            ok = True
            service_booking_instance.check_out_date_time = datetime.now()
            service_booking_instance.save()
            return CheckOutServiceBooking(ok=ok, service_booking=service_booking_instance)        
        return CheckOutServiceBooking(ok=ok, vbooking=None)       

# Create mutations for service bookings
class CreateEvent(graphene.Mutation):
    class Arguments:
        input = EventInput(required=True)

    ok = graphene.Boolean()
    event = graphene.Field(EventType)

    @staticmethod
    @login_required
    # @permission_required('auth.change_user')
    def mutate(root, info, input=None):
        user = info.context.user
        ok = False
        event_instance = Event(
            user_id=user.id, # this must come from the token
            event_name = input.event_name,
            start_date_time = input.start_date_time,
            end_date_time = input.end_date_time,
            event_metadata = json.dumps(input.event_metadata),
        )
        event_instance.save()
        return CreateEvent(ok=ok, event=event_instance)        

class CancelEvent(graphene.Mutation):
    class Arguments:
        event_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @staticmethod
    @login_required
    # @permission_required('auth.change_user')
    def mutate(root, info, event_id):
        ok = False   
        event_instance = Event.objects.get(pk=event_id)     
        if event_instance:
            ok = True
            event_instance.delete()
            return CancelEvent(ok=ok)        
        return CancelEvent(ok=ok) 

class SendSupport(graphene.Mutation):
    class Arguments:
        input = SupportInput(required=True)

    ok = graphene.Boolean()

    @staticmethod
    @login_required
    # @permission_required('auth.change_user')
    def mutate(root, info, input=None):
        user = info.context.user
        hotel = Hotel.objects.get(pk=input.hotel_id)
        ok = False
        msg_plain = render_to_string('email/support.txt', { 'message': input.message, 'hotel': hotel.hotel_name, 'site_name': Site.objects.get_current().domain })
        msg_html = render_to_string('email/support.html', { 'message': input.message, 'hotel': hotel.hotel_name, 'site_name': Site.objects.get_current().domain })

        #Sends an email confirmation to the user’s email address.        
        receivers = []

        #If a hotel is specified, the email is sent to all Hotel Administrators else
        #it is sent to all Global Administrators.
        if input.hotel_id:
            receivers = User.objects.get(is_active=True).filter(user_metadata__hotel_id=input.hotel_id).values_list('email', flat=True)        
        else: 
            receivers = User.objects.get(is_active=True).filter(groups__name='Global Administrators').values_list('email', flat=True)

        receivers.append(user.email)

        send_mail(
            'Support: ' + input.subject,
            msg_plain,
            settings.FROM_EMAIL_ADDRESS,
            [receivers],
            html_message=msg_html,
        )

        ok=True

        return SendSupport(ok=ok)   

class Mutation(graphene.ObjectType):
    create_rating = CreateRating.Field()
    create_event = CreateEvent.Field()
    cancel_event = CancelEvent.Field()
    create_service_booking = CreateServiceBooking.Field()
    cancel_service_booking = CancelServiceBooking.Field()
    check_in_service_booking = CheckInServiceBooking.Field()
    check_out_service_booking = CheckOutServiceBooking.Field()
    send_support = SendSupport.Field()