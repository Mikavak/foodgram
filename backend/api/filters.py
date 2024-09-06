import django_filters

from api.models import Ingredient, Recept, Tag


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = []


class ReceptFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(
        field_name='author',
        lookup_expr='exact')
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug')
    is_favorited = django_filters.rest_framework.filters.BooleanFilter(
        method='filter_is_favorited')
    is_in_shopping_cart = django_filters.rest_framework.filters.BooleanFilter(
        method='filter_is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated and value:
            return queryset.filter(favorited__user=user).distinct()
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated and value:
            return queryset.filter(cart__user=user).distinct()
        return queryset

    class Meta:
        model = Recept
        fields = ['author',
                  'tags']
