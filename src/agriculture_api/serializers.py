from rest_framework import serializers

from agriculture_api.models import Farmer, Property, Harvest, CultivatedCrop


class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    farmer = FarmerSerializer(read_only=True)

    class Meta:
        model = Property
        fields = '__all__'


class HarvestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harvest
        fields = '__all__'


class CultivatedCropSerializer(serializers.ModelSerializer):
    harvest = HarvestSerializer(read_only=True)

    class Meta:
        model = CultivatedCrop
        fields = '__all__'


class CropInPropertySerializer(serializers.ModelSerializer):
    cultivated_crop = CultivatedCropSerializer(read_only=True)
    property = PropertySerializer(read_only=True)

    class Meta:
        model = CultivatedCrop
        fields = '__all__'


class AreaByStateSerializer(serializers.Serializer):
    state = serializers.CharField(read_only=True)
    total = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)


class PropertyByStateSerializer(serializers.Serializer):
    total = serializers.IntegerField(read_only=True)
    state = serializers.CharField(read_only=True)

    class Meta:
        fields = '__all__'


class AreaByLandUsageSerializer(serializers.Serializer):
    arable_area = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=2)
    vegetation_area = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=2)


class DashboardSerializer(serializers.Serializer):
    total_farms = serializers.IntegerField(read_only=True)
    total_area = serializers.FloatField(read_only=True)
    area_by_state = AreaByStateSerializer(read_only=True, many=True)
    properties_by_state = PropertyByStateSerializer(read_only=True, many=True)
    total_areas_by_land_usage = AreaByLandUsageSerializer(read_only=True)

    class Meta:
        fields = '__all__'
