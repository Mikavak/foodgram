from django.contrib import admin
from persons.models import Follower, Person
from rest_framework.exceptions import ValidationError

from .forms import ReceptForm
from .models import (Cart, Favorite, Ingredient, IngredientRecept, Recept, Tag,
                     TagRecept)


class IngredientReceptInline(admin.TabularInline):
    model = IngredientRecept
    extra = 1


class TagReceptInline(admin.TabularInline):
    model = TagRecept
    extra = 1


class PersonAdmin(admin.ModelAdmin):
    search_fields = ['email', 'first_name']


class ReceptAdmin(admin.ModelAdmin):
    search_fields = ['name', 'author__email']
    list_filter = ('tags',)
    list_display = ('name', 'total_favorites')
    inlines = [IngredientReceptInline, TagReceptInline]
    form = ReceptForm
    #
    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)
    #
    # def save_related(self, request, form, formsets, change):
    #     super().save_related(request, form, formsets, change)
    #     recept = form.instance
    #     if not recept.ingredients.exists():
    #         raise ValidationError(
    #             "Добавить один ингредиент.")
    #     if not recept.tags.exists():
    #         raise ValidationError("Добавить один тэг")
    #     if int(recept.cooking_time) <= DEFAULT:
    #         raise ValidationError("Время не меньше 1 минуты")


class FollowerAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        print(obj.user_id)
        if Follower.objects.filter(user_id=obj.user_id,
                                   following_id=obj.following_id).exists():
            raise ValidationError(
                "Такая подписка уже есть")
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        user = form.instance
        if user.user_id == user.following_id:
            raise ValidationError(
                "Сам на себя не подписаться")


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ['name']


class TagReceptAdmin(admin.ModelAdmin):
    list_filter = ('tag',)
    list_display = ('recept', 'tag')


class IngredientReceptAdmin(admin.ModelAdmin):
    list_display = ('recept', 'ingredient')


class CartAdmin(admin.ModelAdmin):
    list_filter = ('user',)
    list_display = ('recept', 'user')


class FavoriteAdmin(admin.ModelAdmin):
    list_filter = ('user',)
    list_display = ('recept', 'user')


admin.site.register(Tag)
admin.site.register(TagRecept, TagReceptAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recept, ReceptAdmin)
admin.site.register(Follower, FollowerAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(IngredientRecept, IngredientReceptAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
