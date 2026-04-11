from rest_framework import serializers
from .models import Game, Platform, Console

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