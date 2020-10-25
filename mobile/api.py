from rest_framework import viewsets, permissions

from . import serializers
from . import models


class RatingViewSet(viewsets.ModelViewSet):
    """ViewSet for the Rating class"""

    queryset = models.Rating.objects.all()
    serializer_class = serializers.RatingSerializer
    permission_classes = [permissions.IsAuthenticated]


class ServiceBookingViewSet(viewsets.ModelViewSet):
    """ViewSet for the ServiceBooking class"""

    queryset = models.ServiceBooking.objects.all()
    serializer_class = serializers.ServiceBookingSerializer
    permission_classes = [permissions.IsAuthenticated]


class EventViewSet(viewsets.ModelViewSet):
    """ViewSet for the Event class"""

    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    permission_classes = [permissions.IsAuthenticated]
