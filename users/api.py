from rest_framework import viewsets, permissions

from . import serializers
from . import models


class UserMetadataViewSet(viewsets.ModelViewSet):
    """ViewSet for the UserMetadata class"""

    queryset = models.UserMetadata.objects.all()
    serializer_class = serializers.UserMetadataSerializer
    permission_classes = [permissions.IsAuthenticated]
