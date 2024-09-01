import base64

from django.core.files.base import ContentFile
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from rest_framework.response import Response
from rest_framework.validators import UniqueTogetherValidator

from api.models import Tag, Ingredient_Recept, Ingredient, Recept, Tag_Recept
from api.validation import validat
from persons.serializers import PersonSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


# class Ingredient_ReceptSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ingredient_Recept
#         fields = ('amount', )


class IngredientGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


# class SelectRelated:
#     pass


# class IngredientAAASerializer(serializers.ModelSerializer):
#     amount = SlugRelatedField(
#         'amount',
#         source='ingredient_recept',
#         many=True,
#         queryset=Ingredient_Recept.objects.all())
#     # print(serializers)
#     class Meta:
#         model = Ingredient
#         fields = ('id', 'name', 'measurement_unit', 'amount',)
class IngredientofReceptSerializer(serializers.ModelSerializer):
    id = SlugRelatedField('id',
                          source='ingredient',
                          queryset=Ingredient.objects.all())
    name = SlugRelatedField('name',
                            source='ingredient',
                            required=False,
                            read_only=True)
    measurement_unit = SlugRelatedField('measurement_unit',
                                        source='ingredient',
                                        required=False,
                                        read_only=True)
    class Meta:
        model = Ingredient_Recept
        fields = ['id',  'amount', 'name', 'measurement_unit']


class ReceptPostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = PersonSerializer(read_only=True)
    ingredients = IngredientofReceptSerializer(
        source='ingredient_recept_set',
        read_only=True,
        many=True)
    image = Base64ImageField(required=False, allow_null=True)

    def validate(self, data):
        validat(self, data)
        return data

    def create(self, validated_data):
        ing = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recept = Recept.objects.create(**validated_data)
        for tag in tags:
            ta = Tag.objects.get(id=tag)
            Tag_Recept.objects.create(recept=recept, tag=ta)
        for ingredient in ing:
            Ingredient_Recept.objects.create(recept=recept, ingredient_id=ingredient['id'],
                                             amount=ingredient['amount'])
        return recept

    def get_ingredients(self, obj):
        ing = Ingredient_Recept.objects.filter(recept=obj.id)
        ing_serializ = Ingredient_ReceptSerializer(ing, many=True).data
        new_ingredient = []
        for i in ing_serializ:
            ingredient = Ingredient.objects.get(id=i['ingredient'])
            temp_dict = {}
            temp_dict['id'] = ingredient.id
            temp_dict['name'] = ingredient.name
            temp_dict['measurement_unit'] = ingredient.measurement_unit
            temp_dict['amount'] = i['amount']
            new_ingredient.append(temp_dict)
        return new_ingredient

    def update(self, instance, validated_data):
        ing = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        q_t = Tag_Recept.objects.filter(recept=instance)
        q_t.delete()
        for tag in tags:
            t = Tag.objects.get(id=tag)
            Tag_Recept.objects.create(recept=instance, tag=t)
        q_ing = Ingredient_Recept.objects.filter(recept=instance)
        q_ing.delete()
        for ingredient in ing:
            i = Ingredient.objects.get(id=ingredient['id'])
            Ingredient_Recept.objects.create(
                recept=instance, ingredient=i, amount=ingredient['amount'])
        return instance

    def perform_create(self, serializer):
        serializer.save(author=self.context['request'].user)

    class Meta:
        model = Recept
        fields = '__all__'
        read_only_fields = ('author', )


class Ingredient_ReceptSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient_Recept
        fields = ('amount', 'ingredient')


class ReceptReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = PersonSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)


    def get_ingredients(self, obj):
        ing = Ingredient_Recept.objects.filter(recept=obj)
        i = Ingredient_ReceptSerializer(ing, many=True).data
        for r in i:
            r['id'] = Ingredient.objects.get(id=r['ingredient']).pk
            r['name'] = Ingredient.objects.get(id=r['ingredient']).name
            r['measurement_unit'] = Ingredient.objects.get(
                id=r['ingredient']).measurement_unit
            r.pop('ingredient')
        return i

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
        fields = ('id', 'name', 'image', 'cooking_time')