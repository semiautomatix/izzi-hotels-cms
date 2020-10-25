# dashboard.py

from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard
from dashboard_modules import ConfirmedBookings, CancelledBookings,\
    BookingsByNationality, BookingsByGender, BookingsByAgeRange, BookingTrend,\
    MeetingRoomBookings, CoShareBookings
    #''', BookingsByAgeRange, BookingsByNationality,\
    #BookingsByGender, BookingTrend, MeetingRoomBookings, CoShareBookings, 
    #'''


class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.available_children.append(ConfirmedBookings)
        self.available_children.append(CancelledBookings)
        self.available_children.append(BookingsByNationality)
        self.available_children.append(BookingsByGender)
        self.available_children.append(BookingsByAgeRange)    
        self.available_children.append(BookingTrend)      
        self.available_children.append(MeetingRoomBookings)
        self.available_children.append(CoShareBookings) 
