from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

def slug_field_factory(slug_field,many=True):
    return serializers.SlugRelatedField(
        many=many,
        read_only=True,
        slug_field=slug_field
    )

slug_platforms = slug_field_factory('platform_name')
slug_genres = slug_field_factory('genre_name')
slug_consoles = slug_field_factory('console_name')
slug_platform_single = slug_field_factory('platform_name', many=False)

class GameSerializer(serializers.ModelSerializer):
    genres = slug_genres
    platforms = slug_platforms
    consoles = slug_consoles
    class Meta:
        model = Game
        fields = '__all__'

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'

class ConsoleSerializer(serializers.ModelSerializer):
    platform = slug_platform_single
    class Meta:
        model = Console
        fields = '__all__'


class HighlightImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['highlight_image_url']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    game_item = GameSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = '__all__'