from django.contrib import admin

from .models import Tag, Ingredient, Tag_Recept, Recept

admin.site.register(Tag)
admin.site.register(Tag_Recept)
admin.site.register(Ingredient)
admin.site.register(Recept)
