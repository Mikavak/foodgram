from django import forms
from django.core.exceptions import ValidationError

from .models import Cart, Favorite, Recept
from .validation import validate_ingredients_amount
from persons.models import Follower


class ReceptForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        cooking_time = cleaned_data.get("cooking_time")
        tags = self.data.getlist('tagrecept_set-0-tag')
        if not tags or not any(tags):
            raise ValidationError("Добавьте хотя бы один таг.")
        if cooking_time is not None and cooking_time < 1:
            self.add_error(
                'cooking_time',
                "Время приготовления должно быть больше 1 минуты.")

        ingredients = self.data.getlist('ingredientrecept_set-0-ingredient')

        if not ingredients or not any(ingredients):
            raise ValidationError("Добавьте хотя бы один ингредиент.")

        validate_ingredients_amount(self.data)

        return cleaned_data

    class Meta:
        model = Recept
        fields = '__all__'


class FollowerForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get(('following_id')) == cleaned_data.get(('user_id')):
            raise ValidationError("Сам на себя нельзя")
        if Follower.objects.filter(
                user_id=cleaned_data.get(('user_id')),
                following_id=cleaned_data.get(('following_id'))):
            raise ValidationError("Такая подписка есть")


class FavoriterForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        if Favorite.objects.filter(
                user=cleaned_data.get(('user')),
                recept=cleaned_data.get(('recept'))):
            raise ValidationError("Такая связка есть")


class CartForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        if Cart.objects.filter(
                user=cleaned_data.get(('user')),
                recept=cleaned_data.get(('recept'))):
            raise ValidationError("Такая связка есть")
