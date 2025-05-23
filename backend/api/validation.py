from django.core.exceptions import ValidationError
from rest_framework import serializers

from api.constant import DEFAULT
from api.models import Ingredient, Tag


def validate(self, data):
    """Валидация вводных данных при создании рецепта"""

    # Валидация Тэги
    if self.initial_data.get('tags') is None:
        raise serializers.ValidationError(
            {'tags': 'В запросе отсутствует поле таг'})
    if len(self.initial_data.get('tags')) == DEFAULT:
        raise serializers.ValidationError({'tags': 'Пустое поле таг'})
    for tag in self.initial_data.get('tags'):
        if not Tag.objects.filter(id=tag):
            raise serializers.ValidationError({
                'ingredients': 'Указан несуществующий таг'})
    a = len(self.initial_data.get('tags')) > len(
        set(self.initial_data.get('tags')))
    if a:
        raise serializers.ValidationError({'tags': 'Повторяется поле таг'})

    # Валидация Ингредиенты
    ingredients = self.initial_data.get('ingredients')
    id_ingredient = []
    if self.initial_data.get('ingredients') is None:
        raise serializers.ValidationError(
            {'ingredients': 'В запросе отсутствует поле ingredients'}
        )
    for ingredient in ingredients:
        if not Ingredient.objects.filter(id=ingredient['id']):
            raise serializers.ValidationError(
                {'ingredients': 'Вы ввели несуществующий ингредиент'}
            )
        if ingredient['amount'] == DEFAULT:
            raise serializers.ValidationError(
                {'ingredients': 'Пустое поле ingredients'}
            )
        id_ingredient.append(ingredient['id'])
        if len(id_ingredient) > len(set(id_ingredient)):
            raise serializers.ValidationError(
                {'ingredients': 'Повторяется поле ingredients'}
            )
    if len(self.initial_data.get('ingredients')) == DEFAULT:
        raise serializers.ValidationError(
            {'ingredients': 'В запросе отсутствует поле ingredients'}
        )

    # Валидация Изображения
    if self.initial_data.get('image') is None:
        raise serializers.ValidationError(
            {'image': 'Нет картинки'})

    # Валидация Время приготовления
    if self.initial_data.get('cooking_time') is None:
        raise serializers.ValidationError(
            {'cooking_time': 'Нет времени'})
    if int(self.initial_data.get('cooking_time')) <= DEFAULT:
        raise serializers.ValidationError({
            'cooking_time': 'Минимальное время приготовления 1 минута'})

    return data


def validate_ingredients_amount(data):
    total_forms = int(data.get('ingredientrecept_set-TOTAL_FORMS', 0))

    for i in range(total_forms):
        amount = data.get(f'ingredientrecept_set-{i}-amount')
        if amount and int(amount) <= 0:
            raise ValidationError('Количество ингредиента не может быть ноль')
