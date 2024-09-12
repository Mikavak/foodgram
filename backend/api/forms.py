from django import forms
from django.core.exceptions import ValidationError

from .models import Recept


class ReceptForm(forms.ModelForm):
    class Meta:
        model = Recept
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        print(self.data)
        cooking_time = cleaned_data.get("cooking_time")

        if cooking_time is not None and cooking_time < 1:
            self.add_error(
                'cooking_time',
                "Время приготовления должно быть больше 1 минуты.")

        ingredients = self.data.getlist('ingredientrecept_set-0-ingredient')

        # Проверяем, что ингредиенты не пустые
        if not ingredients or not any(ingredients):
            raise ValidationError("Добавьте хотя бы один ингредиент.")

        return cleaned_data
