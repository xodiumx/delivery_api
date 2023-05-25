from django_filters import rest_framework as filter

from .models import Cargo


class CargoFilter(filter.FilterSet):
    """
    Фильтрация грузов по:
        - weight: весу - меньше или равно заданному
        - distance: мили ближайших машин до грузов
    """
    weight = filter.NumberFilter(
        field_name='weight',
        lookup_expr='lte'
    )
    distance = filter.NumberFilter(
        field_name='distance',
        method='filter_distance'
    )

    class Meta:
        model = Cargo
        fields = ('weight', 'distance')

    def filter_distance(self, queryset, name, value):
        # TODO: мили ближайших машин до грузов
        # (Не понял, как это связано с фильтрами)
        return queryset
