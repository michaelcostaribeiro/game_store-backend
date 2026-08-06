from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models, serializers
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
import mercadopago

from .permissions import IsAdminOrReadOnly
from .serializers import CartItemSerializer


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

@api_view(['GET','POST','PATCH', 'DELETE'])
@permission_classes([IsAdminOrReadOnly])
def game(request, id=None):
    if id:
        game_instance = models.Game.objects.get(id=id)
    if request.method == 'GET':
        try:
            serializer = serializers.GameSerializer(game_instance)

            if serializer:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except :
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        serializer = serializers.GameWriteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        serializer = serializers.GameWriteSerializer(game_instance,
                                                     data=request.data,
                                                     partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        game_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def games_model(request):
    genres = models.Genre.objects.values_list('genre_name', flat=True).distinct()
    platforms = models.Platform.objects.values_list('platform_name', flat=True).distinct()
    consoles = models.Console.objects.values_list('console_name', flat=True).distinct()

    return Response({
        "genres": list(genres),
        "platforms": list(platforms),
        "consoles": list(consoles)
    }, status=status.HTTP_200_OK)



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
@permission_classes([IsAuthenticated])
def isAdmin(request):
    user = request.user
    return Response({"is_admin": user.is_staff or user.is_superuser},status=status.HTTP_200_OK)

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

@api_view(['POST','DELETE'])
@permission_classes([IsAuthenticated])
def manage_cart_items(request,item_id=None):
    user_cart = models.Cart.objects.get(user=request.user)
    user_cart_items = list(user_cart.items.all())

    if request.method == 'POST':
        requested_game_id = request.data.get('game_item_id')

        for item in user_cart_items:
            if requested_game_id == item.game_item.id:
                return Response({"detail": "O carrinho do usuário ja possui este item!"},
                                 status=status.HTTP_403_FORBIDDEN)

        serializer = CartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(cart=user_cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        game_searched = models.Game.objects.get(id=item_id)
        for item in user_cart_items:
            if item.game_item.id == game_searched.id:
                item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def gameSearch(request,query):
    try:
        filtered_games = models.Game.objects.filter(title__icontains=query)

        if filtered_games.exists():
            serializer = serializers.GameSerializer(filtered_games, many=True)
            return Response({"games": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

class CreateViewPreference(APIView):
    def post(self, request):
        sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

        cart_data = request.data.get('items', [])

        items_preference = []
        for item in cart_data:
            items_preference.append({
                'id': str(item.get('id')),
                'title': str(item.get('title')),
                'quantity': 1,
                'unit_price': float(item.get('price')),
                'currency_id': 'BRL'
            })


        preference_data = {
            'items': items_preference,
            'back_urls': {
                "success": "https://grid-eldest-fester.ngrok-free.dev/sucesso",
                "failure": "https://grid-eldest-fester.ngrok-free.dev/falha",
                "pending": "https://grid-eldest-fester.ngrok-free.dev/pendente"
            },
            "auto_return": "approved",
            "notification_url": "https://www.google.com",
            "external_reference": "PEDIDO-999"
        }
        try:
            mp_response = sdk.preference().create(preference_data)

            if mp_response.get("status") in [200, 201]:
                preference = mp_response['response']
                return Response({'preference_id': preference['id']}, status=status.HTTP_201_CREATED)
            else:
                return Response({'erro_mercado_pago': mp_response}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MercadoPagoWebhookView(APIView):
    def post(self, request):
        action = request.data.get("action")
        data_id = request.data.get("data", {}).get("id")

        if action == "payment.created" or request.GET.get("topic") == "payment":
            payment_id = data_id or request.GET.get("id")

            sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
            informacao_pagamento = sdk.payment().get(payment_id)["response"]

            status_pagamento = informacao_pagamento["status"]
            referencia_interna = informacao_pagamento.get("external_reference")

            if status_pagamento == "approved":
                print(f"Pedido {referencia_interna} foi aprovado com sucesso!")
            elif status_pagamento == "rejected":
                print(f"Pedido {referencia_interna} foi recusado.")
        return Response(status=status.HTTP_200_OK)