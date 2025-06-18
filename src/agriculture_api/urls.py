from django.urls import path
from rest_framework.routers import DefaultRouter

from agriculture_api.views import (
    FarmerViewSet, PropertyViewSet, HarvestViewSet, CultivatedCropViewSet,
    CropInPropertyViewSet, DashboardView
)

router = DefaultRouter()
router.register('farmers', FarmerViewSet)
router.register('properties', PropertyViewSet)
router.register('harvests', HarvestViewSet)
router.register('cultivated-crops', CultivatedCropViewSet)
router.register('crops-in-properties', CropInPropertyViewSet)

urlpatterns = [
    path('dashboard/', DashboardView.as_view()),
]

urlpatterns += router.urls
