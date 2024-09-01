from django.contrib.auth import get_user_model
from django.shortcuts import render
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from followers.models import Follower
from followers.sereliazers import FollowerPostSerializer

Person = get_user_model()

class FollowerViewSet(ModelViewSet):
    queryset = Follower.objects.all()
    serializer_class = FollowerPostSerializer

    # @action(detail=False,
    #         methods=['GET'],
    #         url_path='subscriptions',
    #         url_name='subscriptions',
    #         permission_classes=[IsAuthenticated])
    # def subscriptions(self, request):
    #     user = request.user
    #     print(user)
    #     list_id_following=Follower.objects.filter(user_id=user)
    #     print(list_id_following)
    #     serializer = FollowerPostSerializer(list_id_following, context={'request': request})
    #     return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):

        user = request.user
        author = get_object_or_404(Person, id=pk)
        if user == author:
            return Response({
                'errors': 'Это Вы'
            }, status=status.HTTP_400_BAD_REQUEST)
        # if Follower.objects.filter(user_id=user, following_id=author).exists():
        #     return Response({
        #         'errors': 'Уже подписаны на этого автора'
        #     }, status=status.HTTP_400_BAD_REQUEST)

        follow_obj=Follower.objects.create(user_id=user, following_id=author)
        serializer = FollowerPostSerializer(follow_obj, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = Follower.objects.filter(user_id=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowerPostSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)




# Create your views here.
