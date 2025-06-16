from django.contrib import admin

from agriculture_api.models import (
    Property, Farmer, CropInProperty, Harvest,
    CultivatedCrop
)


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ("name", "document",)
    search_fields = ("name", "document",)


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("name", "farmer", "city", "state", "vegetation_area", "arable_area", "total_area",)
    search_fields = ("name", "farmer__name", "city", "state",)


@admin.register(Harvest)
class HarvestAdmin(admin.ModelAdmin):
    list_display = ("year",)
    search_fields = ("year",)


@admin.register(CultivatedCrop)
class CultivatedCropAdmin(admin.ModelAdmin):
    list_display = ("name", "harvest__year",)
    search_fields = ("name", "harvest__year",)


@admin.register(CropInProperty)
class CropInPropertyAdmin(admin.ModelAdmin):
    list_display = ("cultivated_crop__name", "property__name", "cultivated_crop__harvest__year",)
