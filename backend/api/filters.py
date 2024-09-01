import django_filters

from api.models import Ingredient, Tag, Recept


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = []

class TagFilter(django_filters.FilterSet):
    #author = django_filters.CharFilter(field_name='author', lookup_expr='exact')
    tags = django_filters.CharFilter(field_name='tags', lookup_expr='exact')

    class Meta:
        model = Recept
        fields = []