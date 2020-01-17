import jwt
import json
import bcrypt


from django.test    import TestCase
from django.test    import Client
from datetime       import datetime
from unittest.mock  import patch, MagicMock

from casetify_backend.settings import SECRET_KEY

from .models            import Order, OrderStatus
from artwokr.models     import 
from user.models        import User
from user.utils         import login_decorator

class UserTest(TestCase):
    def setUp(self): 

        hashed_password = bcrypt.hashpw(('12345678').encode('utf-8'),bcrypt.gensalt())              
        User.objects.create(
            id                  = '1',
            email               = 'ordertest@gmail.com',
            password            = hashed_password,
            name                = "ordertest",
            introduction        = "hello my name is test",
            website             = "http://test.com",
            location            = "Republic of Korea",
            twitter             = "@ordertest",
            image               = "ordertest.jpg",
            mobile_number       = "01022334455",
            first_name          = "test",
            last_name           = "orderpang",
            address             = "seoul",
            zipcode             = "00999"
        )
        Item.objects.create(id="1", name="phone_case")
        DeviceBrand.objects.create(id="1", name="Apple")
        Device.objects.create(id="1", name="iPhone 11 Pro Max")
        Artwork.objects.create(
            id="1", name="Monogram Studio",
            id="2", name="Dusty Pink Loepard Phone Case"
        )
        ArtworkType.objects.create(
            id="1", name="Leather Case",
            id="2", name="Impact Case",
            id="3", name="Ultra Impact Case"
        )
        ArtworkColor.objects.create(
            id="1", name="jet Black",
            id="2", name="#333"
        )
        ArtworkPrice.objects.create(
            id="1", artwork_id="1", device_id="1", price="65.00",
            
        )
        



    def tearDown(self):
        User.objects.filter(email='profiletest@gmail.com').delete()

    def testToken(self):
        test            = {'email':'ordertest@gmail.com', 'password':'12345678'}
        response        = Client().post('/user/signin', json.dumps(test), content_type='applications/json')
        access_token    = response.json()['access_token']
        return access_token

# post ShopBasketAdd
    def test_post_shopbasketadd(self):
        test_token = self.testToken()
        test = {
            'artwork_id'        : '2',
            'artwork_color_id'  : '11',
            'artwork_price_id'  : '1',
            'is_customed'       : 'False',
            'custom_info'       : '',
            'order_status_id'      : '1'
        }
        response        = Client().post('/order/shopbasketadd', json.dumps(test), **{"HTTP_AUTHORIZATION":test_token,"content_type" : "application/json"})
        self.assertEqual(response.status_code, 200)
