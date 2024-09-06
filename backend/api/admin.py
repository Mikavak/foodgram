from django.contrib import admin

from persons.models import Follower, Person

from .models import Ingredient, Recept, Tag, TagRecept

admin.site.register(Tag)
admin.site.register(TagRecept)
admin.site.register(Ingredient)
admin.site.register(Recept)
admin.site.register(Follower)
admin.site.register(Person)
