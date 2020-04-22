from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Status, Report
from project.users.serializers import UserSerializer

class StatusSerializer(serializers.ModelSerializer):
    """
    Serializer for Status object
    """
    class Meta:
        model = Status
        fields = '__all__'
        extra_kwargs = {'name': {'required': True}}

class ReportCreateUpdateSerializer(GeoFeatureModelSerializer):
    """
    Serializer for Status object in create and update action
    This serializer does not use nested status and user object, only id.
    This is because when creating or updating the object, we only need the id of the foregin-key,
        without the details of the foreign-key object..
    """
    class Meta:
        model = Report
        geo_field = 'location'
        fields = '__all__'

class ReportSerializer(GeoFeatureModelSerializer):
    """
    Serializer for Status object in list and retrieve action.
    In this serializer, the user and status foreign-key object is also serialized as a nested object.
    This is because we need the object details in list and retrieve.
    """
    status = StatusSerializer()
    user = UserSerializer()

    class Meta:
        model = Report
        geo_field = 'location'
        fields = '__all__'
        extra_kwargs = {'status': {'required': True}, 'user': {'required': True}}
