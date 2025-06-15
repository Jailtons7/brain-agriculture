from rest_framework import viewsets

from agriculture_api.serializers import (
    FarmerSerializer, PropertySerializer, HarvestSerializer,
    CultivatedCropSerializer, CropInPropertySerializer
)
from agriculture_api.models import (
    Farmer, Property, CultivatedCrop, Harvest, CropInProperty,
)


class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class HarvestViewSet(viewsets.ModelViewSet):
    queryset = Harvest.objects.all()
    serializer_class = HarvestSerializer


class CultivatedCropViewSet(viewsets.ModelViewSet):
    queryset = CultivatedCrop.objects.all()
    serializer_class = CultivatedCropSerializer


class CropInPropertyViewSet(viewsets.ModelViewSet):
    queryset = CropInProperty.objects.all()
    serializer_class = CropInPropertySerializer
