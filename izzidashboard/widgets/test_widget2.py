import json

from jet.dashboard.modules import DashboardModule
from django.db.models import Count
from django.db.models.functions import Cast
from django.db.models.fields import DateField
from django.core.serializers.json import DjangoJSONEncoder
from mobile.models import ServiceBooking
from users.models import UserMetadata

class TestWidget2(DashboardModule):
    title = 'Test2'
    template = 'cms/dashboard_modules/test2.html'    

    def __init__(self, title=None, children=list(), **kwargs):
        services = ServiceBooking.objects.filter(service__service_type='meeting_room')\
                    .values('service__hotel_group__hotel_group_name', 'service__hotel_group_id', start_date=Cast('start_date_time', DateField()))\
                    .annotate(total=Count('id')) 

        hotel_groups=list(services)

        kwargs.update({'children': {'hotel_groups': json.dumps(
            hotel_groups,
            sort_keys=True,
            indent=1,
            cls=DjangoJSONEncoder            
        )}})       
         
        '''
        hotel_groups=[{'name': booking['hotel_group__hotel_group_name'], 'y': booking['total'],\
            'drilldown': booking['hotel_group_id']} for booking in list(bookings)]

        drilldown_hotels = []

        for hotel_group in hotel_groups: 
            services = ServiceBooking.objects.filter(service__service_type='meeting_room').filter(hotel_group_id=hotel_group['drilldown'])\
                        .values('service__hotel__hotel_name', 'service__hotel_id', 'start_date_time')                        
            hotels=[[booking['hotel__hotel_name'], booking['total']] for booking in list(bookings)]
            drilldown_hotels.append({'id': hotel_group['drilldown'], 'data': hotels})

        drilldown_cities = []

        for hotel_group in hotel_groups: 
            services = ServiceBooking.objects.filter(service__service_type='meeting_room').filter(hotel_group_id=hotel_group['drilldown'])\
                        .values('service__hotel_city', 'start_date_time')                        
            cities=[[booking['hotel__city'], booking['total']] for booking in list(bookings)]
            drilldown_cities.append({'id': hotel_group['drilldown'], 'data': cities})                    

        kwargs.update({'children': {'hotel_groups': json.dumps(hotel_groups), 'drilldown_hotels': json.dumps(drilldown_hotels),\
            'drilldown_cities': json.dumps(drilldown_cities)}}) 
        '''
        super(TestWidget2, self).__init__(title, **kwargs)   