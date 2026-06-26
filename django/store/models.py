from django.db import models
from django.conf import settings
from django.db.models import Q
from django.core.exceptions import ValidationError



class Genre(models.Model):
    genre_name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.genre_name

class Platform(models.Model):
    platform_name = models.CharField(max_length=20, unique=True)
    platform_icon = models.URLField(blank=False)
    highlight_image_url = models.URLField(blank=False)
    def __str__(self):
        return self.platform_name

class Console(models.Model):
    console_name = models.CharField(max_length=20, unique=True)
    release_date = models.DateField()
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE,related_name='consoles')

    def __str__(self):
        return self.console_name

class Game(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    genres = models.ManyToManyField(Genre, related_name='games')
    developer = models.CharField(max_length=40)
    release_date = models.DateField()
    platforms = models.ManyToManyField(Platform, related_name='games')
    consoles = models.ManyToManyField(Console, related_name='games')
    img_url = models.URLField(blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity_sold = models.IntegerField()
    def __str__(self):
        return self.title

# class DeviceType(models.Model):
#     type_name = models.CharField(max_length=20, unique=True)
#     def __str__(self):
#         return self.type_name

# class Device(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True)
#     type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
#     img_url = models.URLField(blank=False)
#     price = models.DecimalField(max_digits=6, decimal_places=2)
#     def __str__(self):
#         return self.name

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Carrinho de {self.user}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    game_item = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True)
    # device_item = models.ForeignKey(Device, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()

    # class Meta:
    #     constraints = [
    #         models.CheckConstraint(
    #             condition=(
    #                     Q(game_item__isnull=False, device_item__isnull=True) |
    #                     Q(game_item__isnull=True, device_item__isnull=False)
    #             ),
    #             name='check_single_item_type'
    #         )
    #     ]

    # def clean(self):
    #     if self.game_item and self.device_item:
    #         raise ValidationError("Um item do carrinho não pode ser um jogo e um periférico ao mesmo tempo.")
    #     if not self.game_item and not self.device_item:
    #         raise ValidationError("Você deve selecionar um jogo ou um periférico para adicionar ao carrinho.")

    def __str__(self):
        return f'{self.game_item} - {self.cart}'
        # if self.game_item:
        #     return f'{self.game_item} - {self.cart}'
        # elif self.device_item:
        #     return f'{self.device_item} - {self.cart}'

# class Order(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     order_number = models.IntegerField(null=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     finished = models.BooleanField(default=False)
#     status = models.CharField(max_length=20, default="Recebido")
#
#     def __str__(self):
#         return f'Pedido {self.order_number} de: {self.user.name}'
#
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
#     game = models.ForeignKey(Game, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     price_at_purchase = models.DecimalField(max_digits=6, decimal_places=2)
#
#     def __str__(self):
#         return f'{self.quantity}x {self.game.name} no Pedido #{self.order.order_number}'

