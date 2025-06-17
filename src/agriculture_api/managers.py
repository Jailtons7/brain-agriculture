from django.db.models import Sum, Count
from django.db.models.manager import Manager


class PropertyManager(Manager):
    def get_dashboard(self, filters=None):
        queryset = super().get_queryset()
        if filters:
            queryset = queryset.filter(**filters)

        total_farms = queryset.count()
        total_area = queryset.aggregate(
            sum=Sum('total_area')
        )
        properties_by_state = (
            queryset
            .values('state')
            .annotate(
                total=Count('id')
            )
            .order_by('total')
        )
        areas_by_state = (
            queryset
            .values('state')
            .annotate(
                total=Sum('total_area'),
                arable_area=Sum('arable_area'),
                vegetation_area=Sum('vegetation_area'),
            )
            .order_by('total')
        )

        areas_per_usage = queryset.aggregate(
            arable_area=Sum('arable_area'),
            vegetation_area=Sum('vegetation_area'),
        )

        return {
            'total_farms': total_farms,
            'total_area': total_area['sum'],
            'properties_by_state': list(properties_by_state),
            'areas_by_state': list(areas_by_state),
            'total_areas_by_land_usage': areas_per_usage,
        }


class CultivatedCropManager(Manager):
    def get_top_cultivated_crops(self, filters=None):
        queryset = self.get_queryset()
        if filters:
            queryset = queryset.filter(**filters)

        queryset = (
            queryset
            .annotate(
                total_farms=Count('cropinproperty__property__id')
            )
            .values('name', 'total_farms')
            .order_by('-total_farms')
        )
        return queryset[:10]
