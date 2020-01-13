from django.db import models

from user.models      import User


class Item(models.Model):
    item_name = models.CharField(max_length = 500)

    class Meta:
        db_table = 'items'


class PhoneType(models.Model):
    phonetype_name = models.CharField(max_length = 500)
    vendor_name    = models.CharField(max_length = 500)

    class Meta:
        db_table = 'phone_types'


class PhoneBodyColor(models.Model):
    phonetype_id         = models.ForeignKey('PhoneType', on_delete = models.SET_NULL, null=True)
    phonebody_color_name = models.CharField(max_length = 500)

    class Meta:
        db_table = 'phonebody_colors'


class Artist(models.Model):
    artist_name = models.CharField(max_length = 500)

    class Meta:
        db_table = 'artists'


class Product(models.Model):
    item_id       = models.ForeignKey(Item, on_delete = models.SET_NULL, null = True)
    is_customed   = models.NullBooleanField(null = True)
    custom_option = models.TextField(null = True)
    phonetype_id  = models.ForeignKey(PhoneType, on_delete = models.SET_NULL, null = True)
    artist_id     = models.ForeignKey(Artist, on_delete = models.SET_NULL, null = True)
    introduction  = models.TextField(null = True)
    created_at    = models.DateTimeField(auto_now_add = True)
    updated_at    = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'products'


class ProductReview(models.Model):
    product_id    = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True)
    user_id       = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    rate          = models.PositiveSmallIntegerField(null = True)
    comment_title = models.CharField(max_length = 500, null = True)
    comment_text  = models.CharField(max_length = 500, null = True)
    is_buyer      = models.NullBooleanField(null=True)

    class Meta:
        db_table = 'product_reviews'


class CustomProductImage(models.Model):
    product_id         = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True)
    product_color_id   = models.PositiveSmallIntegerField(null = True)
    product_color_name = models.CharField(max_length = 500, null = True)
    image_1            = models.URLField(max_length = 2500, null = True)
    imgae_2            = models.URLField(max_length = 2500, null = True)
    image_3            = models.URLField(max_length = 2500, null = True)
    image_4            = models.URLField(max_length = 2500, null = True)
    image_5            = models.URLField(max_length = 2500, null = True)

    class Meta:
        db_table = 'custom_product_images'


class RegularProductImage(models.Model):
    product_id         = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True)
    product_color_id   = models.PositiveSmallIntegerField(null = True)
    product_color_name = models.CharField(max_length = 500, null = True)
    phonebody_color_id = models.ForeignKey(PhoneBodyColor, on_delete = models.SET_NULL, null = True)
    image_1            = models.URLField(max_length = 2500, null = True)
    imgae_2            = models.URLField(max_length = 2500, null = True)
    image_3            = models.URLField(max_length = 2500, null = True)
    image_4            = models.URLField(max_length = 2500, null = True)
    image_5            = models.URLField(max_length = 2500, null = True)

    class Meta:
        db_table = 'regualr_product_images'




