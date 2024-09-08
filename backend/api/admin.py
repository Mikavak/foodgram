from django.contrib import admin
from persons.models import Follower, Person

from .models import Ingredient, Recept, Tag, TagRecept


class PersonAdmin(admin.ModelAdmin):
    search_fields = ['email', 'first_name']


class ReceptAdmin(admin.ModelAdmin):
    search_fields = ['name', 'author__email']
    list_filter = ('tags',)
    list_display = ('name', 'total_favorites')


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(Tag)
admin.site.register(TagRecept)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recept, ReceptAdmin)
admin.site.register(Follower)
admin.site.register(Person, PersonAdmin)
