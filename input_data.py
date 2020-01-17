import csv
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "casetify_backend.settings")

import django
django.setup()

from artwork.models import *


CSV_PATH = 'items.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        #print(row)
        Item.objects.create(
            name = row['item_name']
        )

CSV_PATH = 'device_brands.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        #print(row)
        DeviceBrand.objects.create(
            name = row['device_brand_name']
        )

CSV_PATH = 'devices.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        #print(row)
        Device.objects.create(
            name = row['device_name']
        )

CSV_PATH = 'artwork_types.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        #print(row)
        ArtworkType.objects.create(
            name = row['artwork_type_name']
        )

CSV_PATH = 'artwork_colors.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        #print(row)
        ArtworkColor.objects.create(
            name = row['artwork_color_name'],
            info = row['artwork_color_info']
        )

CSV_PATH = 'artists.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        #print(row)
        Artist.objects.create(
            name = row['artist_name'],
            description = row['artist_des']
        )

CSV_PATH = 'device_colors.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        #print(row)
        DeviceColor.objects.create(
            device_id = row['device_id'],
            name = row['device_color_name']
        )

CSV_PATH = 'artworks.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        #print(row)
        Artwork.objects.create(
            name    = row['artwork_name'],
            item_id         = row['item_id'],
            device_id       = row['device_id'],
            artwork_type_id = row['artwork_type_id'],
            artist_id       = row['artist_id'],
            is_customed     = row['is_customed'],
            custom_option   = row['custom_option'],
            introduction    = row['introduction']
        )

CSV_PATH = 'artwork_prices.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        #print(row)
        ArtworkPrice.objects.create(
            artwork_id = row['artwork_id'],
            device_id  = row['device_id'],
            price      = row['price']
        )

CSV_PATH = 'custom_artwork_images.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        #print(row)
        CustomArtworkImage.objects.create(
            artwork_id       = row['artwork_id'],
            artwork_color_id = row['artwork_color_id'],
            image_1          = row['image_1'],
            image_2          = row['image_2'],
            image_3          = row['image_3'],
            image_4          = row['image_4'],
            image_5          = row['image_5'],
        )

CSV_PATH = 'regular_artwork_images.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        #print(row)
        RegularArtworkImage.objects.create(
            artwork_id       = row['artwork_id'],
            artwork_color_id = row['artwork_color_id'],
            device_color_id  = row['device_color_id'],
            image_1          = row['image_1'],
            image_2          = row['image_2'],
            image_3          = row['image_3'],
            image_4          = row['image_4'],
            image_5          = row['image_5'],
        )

CSV_PATH = 'artwork_reviews.csv'
with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        #print(row)
        ArtworkReview.objects.create(
            user_id       = row['user_id'],
            rate          = row['rate'],
            comment_title = row['comment_title'],
            comment_text  = row['comment_text'],
            is_buyer      = row['is_buyer']
        )

