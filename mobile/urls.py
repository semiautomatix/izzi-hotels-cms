from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


router = routers.DefaultRouter()
router.register("Rating", api.RatingViewSet)
router.register("ServiceBooking", api.ServiceBookingViewSet)
router.register("Event", api.EventViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("mobile/Rating/", views.RatingListView.as_view(), name="mobile_Rating_list"),
    path("mobile/Rating/create/", views.RatingCreateView.as_view(), name="mobile_Rating_create"),
    path("mobile/Rating/detail/<int:pk>/", views.RatingDetailView.as_view(), name="mobile_Rating_detail"),
    path("mobile/Rating/update/<int:pk>/", views.RatingUpdateView.as_view(), name="mobile_Rating_update"),
    path("mobile/ServiceBooking/", views.ServiceBookingListView.as_view(), name="mobile_ServiceBooking_list"),
    path("mobile/ServiceBooking/create/", views.ServiceBookingCreateView.as_view(), name="mobile_ServiceBooking_create"),
    path("mobile/ServiceBooking/detail/<int:pk>/", views.ServiceBookingDetailView.as_view(), name="mobile_ServiceBooking_detail"),
    path("mobile/ServiceBooking/update/<int:pk>/", views.ServiceBookingUpdateView.as_view(), name="mobile_ServiceBooking_update"),
    path("mobile/Event/", views.EventListView.as_view(), name="mobile_Event_list"),
    path("mobile/Event/create/", views.EventCreateView.as_view(), name="mobile_Event_create"),
    path("mobile/Event/detail/<int:pk>/", views.EventDetailView.as_view(), name="mobile_Event_detail"),
    path("mobile/Event/update/<int:pk>/", views.EventUpdateView.as_view(), name="mobile_Event_update"),
)
