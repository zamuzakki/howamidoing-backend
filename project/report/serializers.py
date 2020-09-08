from rest_framework import serializers
from rest_framework_gis.serializers import GeometryField
from .models.status import Status
from .models.report import Report
from .models.user import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User object.
    """

    class Meta:
        model = User
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    """
    Serializer for Status object
    """
    class Meta:
        model = Status
        fields = '__all__'


class ReportCreateSerializer(serializers.Serializer):
    """
    Serializer for Report object in create action
    This serializer does not use nested status and user object, only id.
    location is the location of the report,that will be mapped/converted to grid ID
    """
    location = GeometryField()
    status = serializers.IntegerField()
    user = serializers.UUIDField()

    class Meta:
        fields = ('status', 'user', 'location')


class ReportSerializer(serializers.ModelSerializer):
    """
    Default Serializer for Report object.
    """

    class Meta:
        model = Report
        fields = '__all__'


class ReportRetrieveListSerializer(serializers.ModelSerializer):
    """
    Serializer for Report object in list and retrieve action.
    In this serializer, the user and status foreign-key object is also serialized as a nested object.
    This is because we need the object details in list and retrieve.
    """
    status = StatusSerializer()

    class Meta:
        model = Report
        fields = '__all__'
