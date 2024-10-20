from .models import UserProfile, UserAnalyzer
from rest_framework import serializers
import uuid


class RequestDetailsSerializer(serializers.Serializer):
    user_agent = serializers.CharField(max_length=255)
    source_ip = serializers.CharField(max_length=45)
    request_id = serializers.UUIDField()


class RequestSerializer(serializers.Serializer):
    analyzer_id = serializers.UUIDField(required=True)
    phone_number = serializers.CharField(max_length=11, required=True)
    request_details = RequestDetailsSerializer(required=True)


class ResponseSerializer(serializers.ModelSerializer):
    request_id = serializers.UUIDField()
    message = serializers.CharField(default="Success")

    class Meta:
        model = UserProfile
        fields = (
            "natoinal_id",
            "request_id",
            "phonenumber",
            "first_name",
            "last_name",
            "birthday",
            "address",
            "message",
        )
