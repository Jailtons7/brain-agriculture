from rest_framework import serializers

from agriculture_api.models import (
    Farmer, Property, Harvest, CultivatedCrop, CropInProperty
)
from agriculture_api.validators import AREAS_ERROR_MESSAGE


class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    farmer = serializers.PrimaryKeyRelatedField(queryset=Farmer.objects.all())

    class Meta:
        model = Property
        fields = '__all__'

    def validate(self, attrs):
        arable_area = attrs.get('arable_area', 0)
        vegetation_area = attrs.get('vegetation_area', 0)
        total_area = attrs.get('total_area', 0)

        total_sub_areas = (arable_area or 0) + (vegetation_area or 0)
        if total_sub_areas > (total_area or 0):
            raise serializers.ValidationError(AREAS_ERROR_MESSAGE)
        return attrs


class HarvestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harvest
        fields = '__all__'


class CultivatedCropSerializer(serializers.ModelSerializer):
    harvest = serializers.PrimaryKeyRelatedField(queryset=Harvest.objects.all())

    class Meta:
        model = CultivatedCrop
        fields = '__all__'


class CropInPropertySerializer(serializers.ModelSerializer):
    cultivated_crop = serializers.PrimaryKeyRelatedField(queryset=CultivatedCrop.objects.all())
    property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all())

    class Meta:
        model = CropInProperty
        fields = '__all__'


class PropertyByStateSerializer(serializers.Serializer):
    total = serializers.IntegerField(read_only=True)
    state = serializers.CharField(read_only=True)

    class Meta:
        fields = '__all__'


class AreaByLandUsageSerializer(serializers.Serializer):
    arable_area = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=2)
    vegetation_area = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=2)


class AreaByStateSerializer(AreaByLandUsageSerializer):
    state = serializers.CharField(read_only=True)
    total = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)


class TopCultivatedCropsSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    total_farms = serializers.IntegerField(read_only=True)


class DashboardSerializer(serializers.Serializer):
    total_farms = serializers.IntegerField(read_only=True)
    total_area = serializers.FloatField(read_only=True)
    areas_by_state = AreaByStateSerializer(read_only=True, many=True)
    properties_by_state = PropertyByStateSerializer(read_only=True, many=True)
    total_areas_by_land_usage = AreaByLandUsageSerializer(read_only=True)
    top_cultivated_crops = TopCultivatedCropsSerializer(read_only=True, many=True)

    class Meta:
        fields = '__all__'
