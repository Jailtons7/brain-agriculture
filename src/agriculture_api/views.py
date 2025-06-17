from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from agriculture_api.docs import DASHBOARD_VIEW_DESCRIPTION
from agriculture_api.serializers import (
    FarmerSerializer, PropertySerializer, HarvestSerializer,
    CultivatedCropSerializer, CropInPropertySerializer,
    DashboardSerializer,
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


class DashboardView(APIView):
    serializer_class = DashboardSerializer

    @swagger_auto_schema(
        operation_summary="Dashboard Geral",
        operation_description=DASHBOARD_VIEW_DESCRIPTION,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Dados do dashboard",
                schema=DashboardSerializer()
            )
        }
    )
    def get(self, request):
        dashboard_data = Property.objects.get_dashboard()
        dashboard_data.update({"top_cultivated_crops": CultivatedCrop.objects.get_top_cultivated_crops()})
        serialized_data = self.serializer_class(instance=dashboard_data)
        return Response(serialized_data.data)
