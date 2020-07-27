from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometryField
from .models.status import Status
from .models.report import Report
from .models.km_grid import KmGrid
from .models.km_grid_score import KmGridScore
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


class KmGridSerializer(GeoFeatureModelSerializer):
    """
    Serializer for KmGrid object.
    """

    class Meta:
        model = KmGrid
        geo_field = 'geometry'
        fields = '__all__'


class KmGridScoreSerializer(GeoFeatureModelSerializer):
    """
    Serializer for KmGridScore object.
    """

    def to_representation(self, instance):
        feature = dict()
        feature["type"] = "Feature"
        field = self.fields[self.Meta.geo_field]
        feature["geometry"] = field.to_representation(instance.centroid)
        feature["properties"] = {
            "total_score": instance.total_score,
            "total_report": instance.total_report
        }

        return feature

    class Meta:
        model = KmGridScore
        geo_field = 'geometry'
        fields = ('total_score', 'total_report')
