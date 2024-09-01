from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, permissions, serializers
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientFilter, ReceptFilter
from api.models import Tag, Ingredient, Recept, Cart, Favorite
from api.permission import IsOwnerOrReadOnly, IsOwner
from api.serializers import TagSerializer, ReceptReadSerializer, ReceptPostSerializer, \
    IngredientGetSerializer, ReceptCartSerializer
from persons.models import Person
# from persons.serializers import get_absolute_url


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)
    # filterset_class = TagFilter
    http_method_names = ['get']
    # filter_backends =



class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientGetSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)
    filterset_class = IngredientFilter
    http_method_names = ['get']

class Pagin(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'limit'

class ReceptViewSet(viewsets.ModelViewSet):
    queryset = Recept.objects.all()
    pagination_class = Pagin
    filterset_class = ReceptFilter
    filter_backends = (DjangoFilterBackend,)

    # def create(self, request, *args, **kwargs):
    #     print(request.data)
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    # return Response(status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return ReceptPostSerializer
        if self.action == 'list' or self.action == 'retrieve':
            return ReceptReadSerializer

    def get_permissions(self):
        if self.action in ['create','destroy']:
            return (IsOwnerOrReadOnly(),)
        if self.action in ['update','partial_update']:
            return (IsOwner(),)
        return (permissions.AllowAny(),)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response(status=status.HTTP_204_NO_CONTENT)
        if self.request.user == instance.author:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    # def short_url(self, request):

    def perform_create(self, serializer):
        # print(self.request.data)
        # # print(get_absolute_url(self))
        author = Person.objects.get(id=self.request.user.id)
        serializer.save(
            author=author,
            ingredients=self.request.data['ingredients'],
            tags=self.request.data['tags'])

    def perform_update(self, serializer):
        author = Person.objects.get(id=self.request.user.id)
        serializer.save(author=author,
                        ingredients=self.request.data['ingredients'],
                        tags=self.request.data['tags'])

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        if self.request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        id = self.kwargs['pk']
        if not Recept.objects.filter(id=id):
            return Response(status=status.HTTP_404_NOT_FOUND)
        recept = Recept.objects.filter(id=id)[0]
        user = Person.objects.filter(id=self.request.user.id)
        if request.method == 'POST':
            w=Cart.objects.filter(recept=id, user=user[0])
            if not w:
                Cart.objects.create(recept=recept, user=user[0])
                serializer = ReceptCartSerializer(recept)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            cart = Cart.objects.filter(recept=id)
            #recept_not_in_cart = Recept.objects.filter(recept=id)
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
        user = Person.objects.filter(id=self.request.user.id)[0]
        recept = Recept.objects.filter(id=pk)[0]
        if request.method == 'POST':
            if Favorite.objects.filter(recept=recept):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                Favorite.objects.create(user=user, recept=recept)
                serializer = ReceptCartSerializer(recept)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            favor = Favorite.objects.filter(recept=pk)
            if not favor:
                return Response(status=status.HTTP_204_NO_CONTENT)
            favor.delete()
            return Response(status=status.HTTP_400_BAD_REQUEST)




