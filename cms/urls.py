from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


router = routers.DefaultRouter()
router.register("hotel", api.HotelViewSet)
router.register("room", api.RoomViewSet)
router.register("booking", api.BookingViewSet)
router.register("icon", api.IconViewSet)
router.register("service", api.ServiceViewSet)
router.register("hotel_group", api.HotelGroupViewSet)
router.register("hotel_gallery", api.HotelGalleryViewSet)
router.register("booking_trend", api.BookingTrendViewSet, basename="booking_trend")
router.register("co_share_bookings", api.CoShareBookingViewSet, basename="co_share_bookings")
router.register("meeting_room_bookings", api.MeetingRoomBookingViewSet, basename="meeting_room_bookings")

urlpatterns = (    
    # path(r'^image-upload/', views.FileUploadView.as_view()),
    # this is the api url
    path("api/v1/", include(router.urls)),
    # these are for the admin views
    path("cms/hotel/", views.HotelListView.as_view(), name="cms_hotel_list"),
    path("cms/hotel/create/", views.HotelCreateView.as_view(), name="cms_hotel_create"),
    path("cms/hotel/detail/<int:pk>/", views.HotelDetailView.as_view(), name="cms_hotel_detail"),
    path("cms/hotel/update/<int:pk>/", views.HotelUpdateView.as_view(), name="cms_hotel_update"),
    path("cms/room/", views.RoomListView.as_view(), name="cms_room_list"),
    path("cms/room/create/", views.RoomCreateView.as_view(), name="cms_room_create"),
    path("cms/room/detail/<int:pk>/", views.RoomDetailView.as_view(), name="cms_room_detail"),
    path("cms/room/update/<int:pk>/", views.RoomUpdateView.as_view(), name="cms_room_update"),
    path("cms/booking/", views.BookingListView.as_view(), name="cms_booking_list"),
    path("cms/booking/create/", views.BookingCreateView.as_view(), name="cms_booking_create"),
    path("cms/booking/detail/<int:pk>/", views.BookingDetailView.as_view(), name="cms_booking_detail"),
    path("cms/booking/update/<int:pk>/", views.BookingUpdateView.as_view(), name="cms_booking_update"),
    path("cms/icon/", views.IconListView.as_view(), name="cms_icon_list"),
    path("cms/icon/create/", views.IconCreateView.as_view(), name="cms_icon_create"),
    path("cms/icon/detail/<int:pk>/", views.IconDetailView.as_view(), name="cms_icon_detail"),
    path("cms/icon/update/<int:pk>/", views.IconUpdateView.as_view(), name="cms_icon_update"),
    path("cms/service/", views.ServiceListView.as_view(), name="cms_service_list"),
    path("cms/service/create/", views.ServiceCreateView.as_view(), name="cms_service_create"),
    path("cms/service/detail/<int:pk>/", views.ServiceDetailView.as_view(), name="cms_service_detail"),
    path("cms/service/update/<int:pk>/", views.ServiceUpdateView.as_view(), name="cms_service_update"),
    path("cms/hotel_group/", views.HotelGroupListView.as_view(), name="cms_hotel_group_list"),
    path("cms/hotel_group/create/", views.HotelGroupCreateView.as_view(), name="cms_hotel_group_create"),
    path("cms/hotel_group/detail/<int:pk>/", views.HotelGroupDetailView.as_view(), name="cms_hotel_group_detail"),
    path("cms/hotel_group/update/<int:pk>/", views.HotelGroupUpdateView.as_view(), name="cms_hotel_group_update"),
    path("cms/hotel_gallery/", views.HotelGalleryListView.as_view(), name="cms_hotel_gallery_list"),
    path("cms/hotel_gallery/create/", views.HotelGalleryCreateView.as_view(), name="cms_hotel_gallery_create"),
    path("cms/hotel_gallery/detail/<int:pk>/", views.HotelGalleryDetailView.as_view(), name="cms_hotel_gallery_detail"),
    path("cms/hotel_gallery/update/<int:pk>/", views.HotelGalleryUpdateView.as_view(), name="cms_hotel_gallery_update")    
)
