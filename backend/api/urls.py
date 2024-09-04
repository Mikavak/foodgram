from django.contrib.auth import get_user_model
from django.urls import include, path
from rest_framework import routers

from api.views import IngredientViewSet, ReceptViewSet, TagViewSet
from persons.views import PersonViewSet

Person = get_user_model()

app_name = 'api'

api_router = routers.DefaultRouter()
api_router.register('tags', TagViewSet, basename='tags')
api_router.register('ingredients', IngredientViewSet, basename='ingredients')
api_router.register('recipes', ReceptViewSet, basename='recepts')
api_router.register('users', PersonViewSet, basename='users')


urlpatterns = [
    path('', include(api_router.urls)),
    path('', include('djoser.urls')),

]