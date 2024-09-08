import random
from urllib.parse import urljoin

from django.utils.crypto import get_random_string

from api.filters import IngredientFilter, ReceptFilter
from api.models import (Cart, Favorite, Ingredient, IngredientRecept, Recept,
                        Tag)
from api.pagination import Pagin
from api.permission import IsOwner, IsOwnerOrReadOnly
from api.serializers import (IngredientSerializer, ReceptCartSerializer,
                             ReceptPostSerializer, ReceptReadSerializer,
                             TagSerializer)
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.text import slugify
from django_filters.rest_framework import DjangoFilterBackend

from foodgram_backend import settings
from persons.models import Person
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get']


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)
    filterset_class = IngredientFilter
    http_method_names = ['get']


def get_or_create_short_link(recept):
    if recept.short_url:
        return recept.short_url

    short_url = slugify(
        f'{get_random_string(length=5)}')
    recept.short_url = short_url
    recept.save()
    return short_url


class ReceptViewSet(viewsets.ModelViewSet):
    queryset = Recept.objects.all()
    pagination_class = Pagin
    filterset_class = ReceptFilter
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if (self.action == 'create'
                or self.action == 'partial_update'):
            return ReceptPostSerializer
        if (self.action == 'list'
                or self.action == 'retrieve'):
            return ReceptReadSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return (IsOwnerOrReadOnly(),)
        if self.action in ['update', 'partial_update']:
            return (IsOwner(),)
        return (permissions.AllowAny(),)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response(
                status=status.HTTP_204_NO_CONTENT)
        if self.request.user == instance.author:
            instance.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                status=status.HTTP_403_FORBIDDEN)

    def perform_create(self, serializer):
        author = Person.objects.get(
            id=self.request.user.id)
        serializer.save(
            author=author,
            ingredients=self.request.data['ingredients'],
            tags=self.request.data['tags'])

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ReceptPostSerializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        if self.request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        id = self.kwargs['pk']
        if not Recept.objects.filter(id=id):
            return Response(status=status.HTTP_404_NOT_FOUND)
        recept = Recept.objects.get(id=id)
        user = Person.objects.get(id=self.request.user.id)
        if request.method == 'POST':
            w = Cart.objects.filter(recept=id,
                                    user=user)
            if not w:
                Cart.objects.create(recept=recept,
                                    user=user)
                serializer = ReceptCartSerializer(recept)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            cart = Cart.objects.filter(recept=id)
            if not cart:
                return Response(status=status.HTTP_204_NO_CONTENT)
            cart.delete()
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        if self.request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if not Recept.objects.filter(id=pk):
            return Response(status=status.HTTP_404_NOT_FOUND)
        user = Person.objects.get(id=self.request.user.id)
        recept = Recept.objects.get(id=pk)
        if request.method == 'POST':
            if Favorite.objects.filter(recept=recept, user=user):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                Favorite.objects.create(user=user, recept=recept)
                serializer = ReceptCartSerializer(recept)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            favorite = Favorite.objects.filter(recept=pk, user=user)
            if not favorite:
                return Response(status=status.HTTP_204_NO_CONTENT)
            favorite.delete()
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'],
            permission_classes=[permissions.AllowAny],
            url_path='get-link')
    def get_link(self, request, pk=None):
        recept = Recept.objects.get(id=pk)
        short_url = get_or_create_short_link(recept)
        content = {'short-link': short_url}
        return Response(content, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'],)
    def download_shopping_cart(self, request):
        if self.request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        ingredients = IngredientRecept.objects.filter(
            recept__cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        content = 'Список покупок:\n'
        for ingredient in ingredients:
            content += '\n'.join([
                f'{ingredient["ingredient__name"]}'
                f' {ingredient["amount"]}'
                f' {ingredient["ingredient__measurement_unit"]}\n'

            ])
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] \
            = 'attachment; filename="buy_ingredients.txt"'

        return response


def redirect_to_recipe(request, short_url):
    recept = Recept.objects.get(short_url=short_url)
    url = (f'{settings.FRONTEND_URL}/recipes/{recept.id}')
    return redirect(url)
