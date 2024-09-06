import base64

from api.models import Recept
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from persons.models import Follower
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

Person = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class AvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(
        required=True,
        allow_null=True)

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get(
            'avatar',
            instance.avatar)
        instance.save()
        return instance

    class Meta:
        model = Person
        fields = ('avatar',)


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar')


class FollowerReceptSerialezer(serializers.ModelSerializer):
    class Meta:
        model = Recept
        fields = ('id',
                  'name',
                  'image',
                  'cooking_time')


class FollowerPostSerializer(serializers.ModelSerializer):
    email = SlugRelatedField('email',
                             read_only=True,
                             source='following_id')
    id = SlugRelatedField('id',
                          read_only=True,
                          source='following_id')
    username = SlugRelatedField(
        'username',
        read_only=True,
        source='following_id')
    first_name = SlugRelatedField(
        'first_name',
        read_only=True,
        source='following_id')
    last_name = SlugRelatedField(
        'last_name',
        read_only=True,
        source='following_id')
    is_subscribed = SlugRelatedField(
        'is_subscribed',
        read_only=True,
        source='following_id')
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Follower
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar',
            'recipes',
            'recipes_count')

    def get_recipes_count(self, obj):
        return Recept.objects.filter(
            author=obj.following_id.id).count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        list_recept = Recept.objects.filter(
            author=obj.following_id.id)
        if limit:
            list_recept = list_recept[:int(limit)]
        serializer_recipes = FollowerReceptSerialezer(
            list_recept,
            many=True)
        return serializer_recipes.data

    def get_avatar(self, obj):
        if not Person.objects.filter(
                id=obj.following_id.id)[0].avatar:
            return None
        print(self.context.get("request").get_full_path())
        return (
            f'{self.context.get("request").headers.get("Host")}'
            f'/{str(Person.objects.filter(id=obj.following_id.id)[0].avatar)}')
