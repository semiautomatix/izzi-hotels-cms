import json

from jet.dashboard.modules import DashboardModule

class MeetingRoomBookings(DashboardModule):
    title = 'Meeting Room Bookings'
    template = 'cms/dashboard_modules/time_chart_services.html'    

    def __init__(self, title=None, children=list(), **kwargs):
        kwargs.update({'children': {'prefix': 'meeting_room_bookings', 'title': 'Meeting Room Bookings', 'rest_url': '/api/v1/meeting_room_bookings'}})

        super(MeetingRoomBookings, self).__init__(title, **kwargs)   