from django.contrib.auth import get_user_model
from django.db import models

from api.constant import (DEFAULT, MEASUREMENT, NAME_INGREDIENT, NAME_RECEPT,
                          SHORT_URL, TAG_LENGTH)

Person = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=TAG_LENGTH,
        unique=True,
        null=False,
        verbose_name='Название тега')
    slug = models.SlugField(
        max_length=TAG_LENGTH,
        unique=True,
        null=False,
        verbose_name='Слаг')

    class Meta:
        verbose_name_plural = 'Теги'
        verbose_name = 'тег'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=NAME_INGREDIENT,
        unique=True,
        null=False,
        verbose_name='Название ингредиента')
    measurement_unit = models.CharField(
        max_length=MEASUREMENT,
        verbose_name='Мера измерения')

    class Meta:
        verbose_name_plural = 'Ингридиенты'
        verbose_name = 'ингридиент'

    def __str__(self):
        return self.name


class Recept(models.Model):
    author = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='recept',
        verbose_name='Автор рецепта')
    name = models.CharField(
        max_length=NAME_RECEPT,
        verbose_name='Название рецепта')
    image = models.ImageField(
        upload_to='images/',
        verbose_name='Картинка рецепта')
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecept',
        verbose_name='Ингредиенты рецепта')
    tags = models.ManyToManyField(
        Tag,
        through='TagRecept',
        verbose_name='Теги рецепта')
    cooking_time = models.IntegerField(
        default=DEFAULT,
        verbose_name='Время приготовления')
    short_url = models.CharField(
        max_length=SHORT_URL,
        verbose_name='Короткая ссылка',
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Рецепты'
        verbose_name = 'рецепт'

    def __str__(self):
        return self.name


class IngredientRecept(models.Model):
    recept = models.ForeignKey(
        Recept,
        on_delete=models.CASCADE,
        verbose_name='Рецепт')
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент')
    amount = models.IntegerField(
        default=DEFAULT,
        verbose_name='Количество')


class TagRecept(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег')
    recept = models.ForeignKey(
        Recept,
        on_delete=models.CASCADE,
        verbose_name='Рецепт')


class Cart(models.Model):
    user = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
    )
    recept = models.ForeignKey(
        Recept,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Корзина'


class Favorite(models.Model):
    user = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        verbose_name='Пользователь')
    recept = models.ForeignKey(
        Recept,
        on_delete=models.CASCADE,
        related_name='favorited',
        verbose_name='Рецепт')

    class Meta:
        verbose_name = 'Избранное'
