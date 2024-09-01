from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from api.models import Recept
from followers.models import Follower, Person


class FollowerReceptSerialezer(serializers.ModelSerializer):
    class Meta:
        model = Recept
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowerPostSerializer(serializers.ModelSerializer):
    email = SlugRelatedField('email', read_only=True, source='following_id')
    id = SlugRelatedField('id', read_only=True, source='following_id')
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
        return Recept.objects.filter(author=obj.following_id.id).count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        list_recept = Recept.objects.filter(author=obj.following_id.id)
        if limit:
            list_recept = list_recept[:int(limit)]
        serializer_recipes = FollowerReceptSerialezer(list_recept, many=True)
        return serializer_recipes.data

    def get_avatar(self, obj):
        if not Person.objects.filter(id=obj.following_id.id)[0].avatar:
            return None
        print(self.context.get("request").get_full_path())
        return (
            f'{self.context.get("request").headers.get("Host")}'
            f'/{str(Person.objects.filter(id=obj.following_id.id)[0].avatar)}')
