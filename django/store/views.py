from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from . import models, serializers
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken

def store(request):
    data = models.Game.objects.all()
    serializer = serializers.GameSerializer(data, many=True)
    return JsonResponse({'games': serializer.data})

def games_by_platform(request, platform_name):
    data = models.Game.objects.filter(platforms__platform_name__iexact=platform_name)
    serializer = serializers.GameSerializer(data, many=True)
    return JsonResponse({'games': serializer.data})

def hightlight_image_by_platform(request, platform_name):
    data = models.Platform.objects.filter(platform_name__iexact=platform_name).first()
    serializer = serializers.HighlightImageSerializer(data)
    return JsonResponse({'image': serializer.data['highlight_image_url']})

def platform_icons(request):
    data = models.Platform.objects.all()
    serializer = serializers.PlatformSerializer(data, many=True)
    return JsonResponse({'platforms': serializer.data})

def consoles(request):
    data = models.Console.objects.all().order_by('-release_date')
    serializer = serializers.ConsoleSerializer(data, many=True)
    return JsonResponse({'consoles': serializer.data})

def game(request, id):
    data = models.Game.objects.get(id=id)
    serializer = serializers.GameSerializer(data)
    return JsonResponse(serializer.data)

@api_view(['POST'])
def register(request):
    serializer = serializers.UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return Response(tokens,status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def cart(request):
    try:
        user = request.user
        cart = models.Cart.objects.filter(user=user)[0]
        cart_items = models.CartItem.objects.filter(cart=cart.id)

        items_serializer = serializers.CartItemSerializer(cart_items, many=True)


        return Response(items_serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def gameSearch(request,query):
    try:
        filtered_games = []

        for game in models.Game.objects.all():
            if query.lower() in game.title.lower():
                filtered_games.append(game)

        serializer = serializers.GameSerializer(filtered_games, many=True)

        if filtered_games:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)