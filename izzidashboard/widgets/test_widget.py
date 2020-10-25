import json

from jet.dashboard.modules import DashboardModule
from django.db.models import Count
from cms.models import Booking
from users.models import UserMetadata

class TestWidget(DashboardModule):
    title = 'Test'
    template = 'cms/dashboard_modules/pie.html'    

    def __init__(self, title=None, children=list(), **kwargs):
        print("test1")
        bookings = Booking.objects.filter(booking_status=1)\
                    .values('hotel_group__hotel_group_name', 'hotel_group_id') \
                    .annotate(total=Count('hotel_group_id')) 

        hotel_groups=[{'name': booking['hotel_group__hotel_group_name'], 'y': booking['total'],\
            'drilldown': booking['hotel_group_id']} for booking in list(bookings)]
    
        drilldown_hotels = []

        for hotel_group in hotel_groups: 
            bookings = Booking.objects.filter(booking_status=1).filter(hotel_group_id=hotel_group['drilldown'])\
                        .values('hotel_id', 'hotel__hotel_name') \
                        .annotate(total=Count('hotel_id')) 
            hotels=[[booking['hotel__hotel_name'], booking['total']] for booking in list(bookings)]
            drilldown_hotels.append({'id': hotel_group['drilldown'], 'data': hotels})

        drilldown_cities = []

        for hotel_group in hotel_groups: 
            bookings = Booking.objects.filter(booking_status=1).filter(hotel_group_id=hotel_group['drilldown'])\
                        .values('hotel__city') \
                        .annotate(total=Count('hotel__city')) 
            cities=[[booking['hotel__city'], booking['total']] for booking in list(bookings)]
            drilldown_cities.append({'id': hotel_group['drilldown'], 'data': cities})

        kwargs.update({'children': {'hotel_groups': json.dumps(hotel_groups), 'drilldown_hotels': json.dumps(drilldown_hotels),\
            'drilldown_cities': json.dumps(drilldown_cities), 'prefix': 'test'}})  

        super(TestWidget, self).__init__(title, **kwargs)   