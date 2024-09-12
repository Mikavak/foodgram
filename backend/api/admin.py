from django.contrib import admin
from persons.models import Follower, Person

from .forms import CartForm, FavoriterForm, FollowerForm, ReceptForm
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
    list_display = ('name', 'created_at', 'total_favorites')
    inlines = [IngredientReceptInline, TagReceptInline]
    form = ReceptForm


class FollowerAdmin(admin.ModelAdmin):
    form = FollowerForm


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
    form = CartForm


class FavoriteAdmin(admin.ModelAdmin):
    list_filter = ('user',)
    list_display = ('recept', 'user')
    form = FavoriterForm


admin.site.register(Tag)
admin.site.register(TagRecept, TagReceptAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recept, ReceptAdmin)
admin.site.register(Follower, FollowerAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(IngredientRecept, IngredientReceptAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
