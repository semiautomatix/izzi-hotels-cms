from rest_framework import serializers

from . import models


class UserMetadataSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserMetadata
        fields = [
            "age_range",
            "profile_picture",
            "middle_name",
            "profile_picture",
            "created",
            "last_updated",
            "nationality",
            "position",
            "gender",
        ]
