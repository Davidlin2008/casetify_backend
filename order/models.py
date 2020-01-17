from django.db import models

from user.models import User
from artwork.models import Artwork, ArtworkColor, ArtworkPrice

class Order(models.Model):
    user            = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    artwork         = models.ForeignKey(Artwork, on_delete=models.SET_NULL, null=True)
    artwork_color   = models.ForeignKey(ArtworkColor, on_delete=models.SET_NULL, null=True)
    artwork_price   = models.ForeignKey(ArtworkPrice, on_delete=models.SET_NULL, null=True)
    is_customed     = models.BooleanField(null = True)
    custom_info     = models.TextField(max_length = 3000, null = True)
    order_status    = models.ForeignKey('OrderStatus', on_delete=models.SET_NULL, null=True)
    created_at      = models.DateTimeField(auto_now_add = True)
    updated_at      = models.DateTimeField(auto_now = True)
    
    class Meta:
        db_table = 'orders'
    
class OrderStatus(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'orderstatus'