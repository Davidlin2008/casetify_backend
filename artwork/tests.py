import json

from django.test import TestCase, Client
from django.http import JsonResponse, HttpResponse

from artwork.models import *
import *.csv
import input_data

class RegularArtworkList(TestCase):
    def setUp(self):
        client = Client()

        Artwork.objects.create()
        ArtworkType.objects.create()
        ArtworkPriceDevice.objects.create()
        RegularArtworkImage.objects.create()

    def tearDown(self):
        Artwork.objects.all().delete()
        ArtworkType.objects.all().delete()
        ArtworkPriceDevice.objects.all().delete()
        RegularArtworkImage.objects.all().delete()

    def test_haha(self):
        client = Client()

        reponse = client.get('/artwork/regular/list?offset=8&limit=17')
        self.assertEqual(reponse.status_code, 200)
        self.aseertEqual(
            response.json(),
            
        )
