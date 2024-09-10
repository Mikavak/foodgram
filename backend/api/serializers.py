import base64

from api.models import (Cart, Favorite, Ingredient, IngredientRecept, Recept,
                        Tag, TagRecept)
from api.validation import validat
from django.core.files.base import ContentFile
from persons.serializers import PersonSerializer
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id',
                  'name',
                  'measurement_unit',)


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class IngredientReceptSerializer(serializers.ModelSerializer):
    id = SlugRelatedField(
        'id',
        source='ingredient',
        queryset=Ingredient.objects.all())
    name = SlugRelatedField(
        'name',
        source='ingredient',
        required=False,
        read_only=True)
    measurement_unit = SlugRelatedField(
        'measurement_unit',
        source='ingredient',
        required=False,
        read_only=True)

    class Meta:
        model = IngredientRecept
        fields = ['id',
                  'amount',
                  'name',
                  'measurement_unit']


class ReceptPostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        many=True,
        read_only=True)
    author = PersonSerializer(
        read_only=True)
    ingredients = IngredientReceptSerializer(
        source='ingredientrecept_set',
        read_only=True,
        many=True)
    image = (Base64ImageField
             (required=False,
              allow_null=True))
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        return Favorite.objects.filter(
            user=obj.author).exists()

    def get_is_in_shopping_cart(self, obj):
        return Cart.objects.filter(
            user=obj.author).exists()

    def validate(self, data):
        data['ingredients'] = self.initial_data['ingredients']
        data['tags'] = self.initial_data['tags']
        validat(self, data)
        return data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recept = Recept.objects.create(**validated_data)
        for tag in tags:
            tag_model = Tag.objects.get(
                id=tag)
            TagRecept.objects.create(
                recept=recept,
                tag=tag_model)
        for ingredient in ingredients:
            IngredientRecept.objects.create(
                recept=recept,
                ingredient_id=ingredient['id'],
                amount=ingredient['amount'])
        return recept

    def perform_create(self, serializer):
        serializer.save(author=self.context['request'].user)

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')

        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)

        if 'image' in validated_data:
            instance.image = validated_data['image']

        instance.save()

        if ingredients_data:
            IngredientRecept.objects.filter(recept=instance).delete()
            for ingredient in ingredients_data:
                obj_ing = Ingredient.objects.get(id=ingredient['id'])
                IngredientRecept.objects.create(recept=instance,
                                                ingredient=obj_ing,
                                                amount=ingredient['amount'])

        if tags_data:
            TagRecept.objects.filter(recept=instance.id).delete()
            for tag in tags_data:
                obj_tag = Tag.objects.get(id=tag)
                TagRecept.objects.create(recept=instance,
                                         tag=obj_tag)

        return instance

    class Meta:
        model = Recept
        exclude = ('short_url',)
        read_only_fields = ('author', )


class ReceptReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True,
                         read_only=True)
    author = PersonSerializer(read_only=True)
    ingredients = IngredientReceptSerializer(
        source='ingredientrecept_set',
        read_only=True,
        many=True)
    image = Base64ImageField(required=False,
                             allow_null=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_in_shopping_cart(self, obj):
        if self.context.get('request').user.is_authenticated:
            return Recept.objects.filter(
                cart__user=self.context['request'].user,
                id=obj.id).exists()
        return False

    def get_is_favorited(self, obj):
        if self.context.get('request').user.is_authenticated:
            return Recept.objects.filter(
                favorited__user=self.context.get('request').user,
                id=obj.id).exists()
        return False

    class Meta:
        model = Recept
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )


class ReceptCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recept
        fields = ('id',
                  'name',
                  'image',
                  'cooking_time')
