from django.db import models
from django.conf import settings


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

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Carrinho de {self.user}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    game_item = models.ForeignKey(Game, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.game_item} - {self.cart}'

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

