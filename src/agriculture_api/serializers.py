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
