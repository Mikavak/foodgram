from django.contrib.auth import get_user_model
from djoser import permissions
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import (DestroyAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from persons.models import Follower
from persons.serializers import (AvatarSerializer, FollowerPostSerializer,
                                 PersonSerializer)

Person = get_user_model()


class PersonViewSet(UserViewSet):
    pagination_class = LimitOffsetPagination

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(Person, id=id)
        if request.method == 'POST':
            if user == author:
                return Response({
                    'errors': 'Это Вы'
                }, status=status.HTTP_400_BAD_REQUEST)
            if Follower.objects.filter(
                    user_id=user,
                    following_id=author):
                return Response({
                    'errors': 'Уже подписаны на этого автора'
                }, status=status.HTTP_400_BAD_REQUEST)
            follow_obj = Follower.objects.create(
                user_id=user, following_id=author)
            serializer = FollowerPostSerializer(
                follow_obj, context={'request': request})
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            follow_obj = Follower.objects.filter(
                user_id=user,
                following_id=author)
            if not follow_obj:
                return Response({
                    'errors': 'Нет такой подписки'
                }, status=status.HTTP_400_BAD_REQUEST)
            follow_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            permission_classes=[IsAuthenticated],
            methods=['GET'])
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


class AvatarUpdate(UpdateAPIView, DestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = (permissions.CurrentUserOrAdmin, )

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        instance = Person.objects.get(pk=self.request.user.pk)
        instance.avatar = None
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeList(RetrieveAPIView):
    permission_classes = (permissions.CurrentUserOrAdmin, )
    serializer_class = PersonSerializer

    def get_object(self):
        return self.request.user
