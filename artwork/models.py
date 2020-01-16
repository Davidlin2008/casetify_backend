from django.db import models

from user.models import User

class Item(models.Model):
    name = models.CharField(max_length = 500)

    class Meta:
        db_table = 'items'

class Artist(models.Model):
    name        = models.CharField(max_length = 500)
    description = models.CharField(max_length = 500, null = True)

    class Meta:
        db_table = 'artists'

class DeviceBrand(models.Model):
    name = models.CharField(max_length = 500)

    class Meta:
        db_table = 'device_brands'

class Device(models.Model):
    name          = models.CharField(max_length = 500)
    device_brand  = models.ForeignKey(DeviceBrand, on_delete = models.SET_NULL, null = True)
    overlay_image = models.URLField(max_length = 2500) 

    class Meta:
        db_table = 'devices'

class DeviceColor(models.Model):
    name   = models.CharField(max_length = 500)
    device = models.ForeignKey(Device, on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'device_colors'

class ArtworkType(models.Model):
    name = models.CharField(max_length = 2500, null = True)

    class Meta:
        db_table = 'artwork_types'

class Artwork(models.Model):
    name          = models.CharField(max_length = 500)
    item          = models.ForeignKey(Item, on_delete = models.SET_NULL, null = True)
    device        = models.ForeignKey(Device, on_delete = models.SET_NULL, null = True)
    artwork_type  = models.ForeignKey(ArtworkType, on_delete = models.SET_NULL, null = True)
    artist        = models.ForeignKey(Artist, on_delete = models.SET_NULL, null = True)
    is_customed   = models.NullBooleanField(null = True)
    custom_option = models.TextField(max_length = 3000, null = True)
    introduction  = models.TextField(max_length = 2000, null = True)
    created_at    = models.DateTimeField(auto_now_add = True)
    updated_at    = models.DateTimeField(auto_now = True)
    color         = models.ManyToManyField('ArtworkColor', through = 'ArtworkColorArtwork', related_name='artwork_artworkcolor')
    price         = models.ManyToManyField('Device', through = 'ArtworkPrice', related_name='artwork_price')

    class Meta:
        db_table = 'artworks'

class ArtworkColor(models.Model):
    name = models.CharField(max_length = 500)
    info = models.CharField(max_length = 2500, null = True) 

    class Meta:
        db_table = 'artwork_colors'

class ArtworkColorArtwork(models.Model):
    artwork       = models.ForeignKey(Artwork, on_delete = models.SET_NULL, null = True)
    artwork_color = models.ForeignKey(ArtworkColor, on_delete = models.SET_NULL, null = True)
    device        = models.ForeignKey(Device, on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'artwork_color_artworks'

class ArtworkPrice(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete = models.SET_NULL, null = True)
    device  = models.ForeignKey(Device, on_delete = models.SET_NULL, null = True)
    price   = models.DecimalField(max_digits = 18, decimal_places = 2, null = True)

    class Meta:
        db_table = 'artwork_prices'

class CustomArtworkImage(models.Model):
    artwork       = models.ForeignKey(Artwork, on_delete = models.SET_NULL, null = True)
    artwork_color = models.ForeignKey(ArtworkColor, on_delete = models.SET_NULL, null = True)
    image_1       = models.URLField(max_length = 2500, null=True)
    image_2       = models.URLField(max_length = 2500, null=True)
    image_3       = models.URLField(max_length = 2500, null=True)
    image_4       = models.URLField(max_length = 2500, null=True)
    image_5       = models.URLField(max_length = 2500, null=True)
    
    class Meta:
        db_table = 'custom_artwork_images'

class RegularArtworkImage(models.Model):
    artwork       = models.ForeignKey(Artwork, on_delete = models.SET_NULL, null = True)
    artwork_color = models.ForeignKey(ArtworkColor, on_delete = models.SET_NULL, null = True)
    device_color  = models.ForeignKey(DeviceColor, on_delete = models.SET_NULL, null = True)
    image_1       = models.URLField(max_length = 2500, null=True)
    image_2       = models.URLField(max_length = 2500, null=True)
    image_3       = models.URLField(max_length = 2500, null=True)
    image_4       = models.URLField(max_length = 2500, null=True)
    image_5       = models.URLField(max_length = 2500, null=True)

    class Meta:
        db_table = 'regular_artwork_images' 

class ArtworkReview(models.Model):
    artwork       = models.ForeignKey(Artwork, on_delete = models.SET_NULL, null = True)
    user          = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    rate          = models.PositiveSmallIntegerField(null=True)
    comment_title = models.CharField(max_length = 500, null=True)
    comment_text  = models.TextField(max_length = 1000, null=True)
    is_buyer      = models.NullBooleanField(null=True)

    class Meta:
        db_table = 'artwork_reviews'



