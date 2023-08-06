from rest_framework import serializers


class SocialLoginSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, allow_blank=False)
    grant_type = serializers.CharField(required=False, allow_blank=True)
    scope = serializers.CharField(required=False, allow_blank=True)

