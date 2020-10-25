from jet.dashboard.modules import DashboardModule
from plotly import graph_objs
from plotly.offline import plot
from django.db.models import Count
import dash
import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash  

'''
class BookingsByAgeRange(DashboardModule):
    title = 'Bookings by Age Range'
    template = 'cms/dashboard_modules/bookings_by_age_range.html'    
    style = 'height: 650px'    

class BookingsByGender(DashboardModule):
    title = 'Bookings by Gender'
    template = 'cms/dashboard_modules/bookings_by_gender.html'    
    style = 'height: 650px'    

class BookingsByNationality(DashboardModule):
    title = 'Bookings by Nationality'
    template = 'cms/dashboard_modules/bookings_by_nationality.html',
    style = 'height: 650px'  

class BookingTrend(DashboardModule):
    title = 'Booking Trend'
    template = 'cms/dashboard_modules/booking_trend.html'        

class CoShareBookings(DashboardModule):
    title = 'Co-Share Bookings'
    template = 'cms/dashboard_modules/co_share_bookings.html'       

class MeetingRoomBookings(DashboardModule):
    title = 'Meeting Room Bookings'
    template = 'cms/dashboard_modules/meeting_room_bookings.html'               
    style = 'height: 650px'    
'''

from izzidashboard.widgets.test_widget import TestWidget
from izzidashboard.widgets.test_widget2 import TestWidget2
from izzidashboard.widgets.test_widget3 import TestWidget3
from izzidashboard.widgets.test_widget4 import TestWidget4
from izzidashboard.widgets.confirmed_bookings import ConfirmedBookings
from izzidashboard.widgets.cancelled_bookings import CancelledBookings
from izzidashboard.widgets.bookings_by_age_range import BookingsByAgeRange
from izzidashboard.widgets.bookings_by_gender import BookingsByGender
from izzidashboard.widgets.bookings_by_nationality import BookingsByNationality
from izzidashboard.widgets.booking_trend import BookingTrend
from izzidashboard.widgets.co_share_bookings import CoShareBookings
from izzidashboard.widgets.meeting_room_bookings import MeetingRoomBookings