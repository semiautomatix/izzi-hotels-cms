import json

from jet.dashboard.modules import DashboardModule

class CoShareBookings(DashboardModule):
    title = 'Co-share Bookings'
    template = 'cms/dashboard_modules/time_chart_services.html'    

    def __init__(self, title=None, children=list(), **kwargs):
        kwargs.update({'children': {'prefix': 'co_share_bookings', 'title': 'Co-share Bookings', 'rest_url': '/api/v1/co_share_bookings'}})

        super(CoShareBookings, self).__init__(title, **kwargs)   