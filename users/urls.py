from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


router = routers.DefaultRouter()
router.register("UserMetadata", api.UserMetadataViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("users/UserMetadata/", views.UserMetadataListView.as_view(), name="users_UserMetadata_list"),
    path("users/UserMetadata/create/", views.UserMetadataCreateView.as_view(), name="users_UserMetadata_create"),
    path("users/UserMetadata/detail/<int:pk>/", views.UserMetadataDetailView.as_view(), name="users_UserMetadata_detail"),
    path("users/UserMetadata/update/<int:pk>/", views.UserMetadataUpdateView.as_view(), name="users_UserMetadata_update"),
)
