import json

from jet.dashboard.modules import DashboardModule
from django.db.models import Count
from django.db.models.functions import Cast
from django.db.models.fields import DateField
from django.core.serializers.json import DjangoJSONEncoder
from cms.models import Booking
from users.models import UserMetadata

class TestWidget4(DashboardModule):
    title = 'Test4'
    template = 'cms/dashboard_modules/bar_time.html'    

    def __init__(self, title=None, children=list(), **kwargs):
        bookings = Booking.objects.all()\
                    .values('hotel_group__hotel_group_name', 'hotel_group_id', 'hotel__hotel_name', 'hotel_id', 'start_date')\
                    .annotate(total=Count('id')) 

        '''data=list({series_name, series_id, drilldown_name, drilldown_id, y} in list(bookings) )

        kwargs.update({'children': {'data': json.dumps(
            data,
            sort_keys=True,
            indent=1,
            cls=DjangoJSONEncoder            
        ), 'prefix': 'booking_trends', 'title': 'Booking Trends'}})'''       
         
        super(TestWidget4, self).__init__(title, **kwargs)   