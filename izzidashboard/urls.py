from django.urls import path, include

from . import views

# Load demo plotly apps - this triggers their registration
import izzidashboard.widgets.confirmed_bookings    # pylint: disable=unused-import
import izzidashboard.widgets.cancelled_bookings    # pylint: disable=unused-import
import izzidashboard.widgets.bookings_by_age_range    # pylint: disable=unused-import
import izzidashboard.widgets.bookings_by_nationality   # pylint: disable=unused-import
import izzidashboard.widgets.bookings_by_gender    # pylint: disable=unused-import
import izzidashboard.widgets.booking_trend    # pylint: disable=unused-import
import izzidashboard.widgets.co_share_bookings    # pylint: disable=unused-import
import izzidashboard.widgets.meeting_room_bookings    # pylint: disable=unused-import
import izzidashboard.widgets.booking_trend    # pylint: disable=unused-import

urlpatterns = (
  path('', views.index),
)
