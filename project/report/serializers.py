from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Status, Report
from project.users.serializers import UserSerializer

class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = ('id', 'name', 'description')

class ReportSerializer(GeoFeatureModelSerializer):
    status = StatusSerializer()
    user = UserSerializer()

    class Meta:
        model = Report
        geo_field = 'location'
        fields = ('id', 'location', 'status', 'timestamp', 'user', )