import json

from jet.dashboard.modules import DashboardModule
from django.db.models import Count
from cms.models import Booking
from users.models import UserMetadata

class BookingsByNationality(DashboardModule):
    title = 'Bookings by Nationality'
    template = 'cms/dashboard_modules/grouped_column_chart.html'    

    def __init__(self, title=None, children=list(), **kwargs):
        # get metadata for current user
        if kwargs.get('context') and kwargs.get('context').get('user'):
            current_user = kwargs.get('context').get('user')
            user_id = current_user.pk
            user_metadata = UserMetadata.objects.get(user_id=user_id)        

            data = []
            
            # if group or hotel then apply filter
            if current_user.groups.filter(name='Hotel Group Administrators').exists(): 
                hotel_group_id = user_metadata.hotel_group_id
                bookings = Booking.objects.filter(hotel_group_id=hotel_group_id).filter(booking_status=1)\
                    .values('hotel__hotel_name', 'hotel_id', 'hotel__city', 'user__usermetadata__nationality') \
                    .annotate(total=Count('id')) 
                data = list(bookings)
            elif current_user.groups.filter(name='Hotel Administrators').exists(): 
                hotel_id = user_metadata.hotel_id
                bookings = Booking.objects.filter(hotel_id=hotel_id).filter(booking_status=1)\
                    .values('hotel__hotel_name', 'hotel_id', 'hotel__city', 'user__usermetadata__nationality') \
                    .annotate(total=Count('id')) 
                data = list(bookings)
            else:
                bookings = Booking.objects.filter(booking_status=1)\
                    .values('hotel_group__hotel_group_name', 'hotel_group_id', 'hotel__hotel_name', 'hotel_id', 'hotel__city', 'user__usermetadata__nationality') \
                    .annotate(total=Count('id')) 
                data = list(bookings)

            kwargs.update({'children': {'data': json.dumps(data), 'prefix': 'bookings_by_nationality', 'series_label': 'user__usermetadata__nationality'}})         
        
        super(BookingsByNationality, self).__init__(title, **kwargs)   