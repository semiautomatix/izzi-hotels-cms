import json

from jet.dashboard.modules import DashboardModule

class BookingTrend(DashboardModule):
    title = 'Booking Trend'
    template = 'cms/dashboard_modules/time_chart.html'    

    def __init__(self, title=None, children=list(), **kwargs):
        kwargs.update({'children': {'prefix': 'booking_trends', 'title': 'Booking Trends','rest_url': '/api/v1/booking_trend'}})

        super(BookingTrend, self).__init__(title, **kwargs)   