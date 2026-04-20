"""
URL configuration for store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('api/store/', views.store, name='store'),
    path('api/<str:platform_name>/', views.games_by_platform, name='games_by_platform'),
    path('api/icons', views.platform_icons, name='icons'),
    path('api/consoles', views.consoles, name='consoles'),
    path('api/hightlightImage/<str:platform_name>/', views.hightlight_image_by_platform, name='hightlight_image_by_platform'),
    path('api/game/<int:id>/', views.game, name='game'),
]
