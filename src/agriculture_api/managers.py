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
        area_by_state = (
            queryset
            .values('state')
            .annotate(
                total=Sum('total_area')
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
            'area_by_state': list(area_by_state),
            'total_areas_by_land_usage': areas_per_usage,
        }
