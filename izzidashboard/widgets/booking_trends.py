import json

from jet.dashboard.modules import DashboardModule
from django.db.models import Count
from django.db.models.functions import Cast
from django.db.models.fields import DateField
from django.core.serializers.json import DjangoJSONEncoder
from cms.models import Booking
from users.models import UserMetadata

class BookingTrendsWidget(DashboardModule):
    title = 'Booking Trends'
    template = 'cms/dashboard_modules/time_chart.html'    

    def __init__(self, title=None, children=list(), **kwargs):
        kwargs.update({'children': {'prefix': 'booking_trends', 'title': 'Booking Trends'}})
