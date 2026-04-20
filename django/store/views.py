from . import models, serializers
from django.http import JsonResponse

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

