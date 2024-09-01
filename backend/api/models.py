from django.contrib.auth import get_user_model
from django.db import models
Person = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True, null=False)
    slug = models.SlugField(max_length=32, unique=True, null=False)

    class Meta:
        verbose_name_plural = 'Теги'
        verbose_name = 'тег'

    def __str__(self):
        return self.name



class Ingredient(models.Model):
    name = models.CharField(max_length=128, unique=True, null=False)
    measurement_unit = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = 'Ингридиенты'
        verbose_name = 'ингридиент'

    def __str__(self):
        return self.name

class Recept(models.Model):
    author = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='recept')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient, through='Ingredient_Recept')
    tags = models.ManyToManyField(Tag, through='Tag_Recept')
    cooking_time = models.IntegerField(default=0)
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Рецепты'
        verbose_name = 'рецепт'


class Ingredient_Recept(models.Model):
    recept = models.ForeignKey(
        Recept,
        on_delete=models.CASCADE)
        # related_name='ingredient_recept')
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE)
        #related_name='ingredient_recept')
    amount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.amount)

    # class Meta:
    #     ordering = ['-id']
    #     verbose_name = 'Количество ингридиента'
    #     verbose_name_plural = 'Количество ингридиентов'
    #     constraints = [
    #         models.UniqueConstraint(fields=['ingredient', 'recipe'],
    #                                 name='unique ingredients recipe')
    #     ]

class Tag_Recept(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recept = models.ForeignKey(Recept, on_delete=models.CASCADE)

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
        related_name='cart'
    )