import jwt
import json
import bcrypt


from django.test    import TestCase
from django.test    import Client
from datetime       import datetime
from unittest.mock  import patch, MagicMock

from casetify_backend.settings import SECRET_KEY

from .models        import User
from .utils         import login_decorator

class UserTest(TestCase):
    def setUp(self): 

        hashed_password = bcrypt.hashpw(('12345678').encode('utf-8'),bcrypt.gensalt())              
        User.objects.create(
            email='testpy@gmail.com',
            password= hashed_password,
            mobile_number='01099887766'
        )

    def tearDown(self):
        User.objects.filter(email='testpy@gmail.com').delete()

# SignUp test
    def test_user_signup_check(self):
        test        = {'email': 'testpy11@gmail.com', 'password':'12345678', 'mobile_number':'01011223344'}
        response    = Client().post('/user/signup', json.dumps(test), content_type='applications/json')
        self.assertEqual(response.status_code, 200)
    
    def test_user_signup_email_check(self):
        test        = {'email': 'testpy@gmail.com', 'password':'12345678', 'mobile_number':'01091223344'}
        response    = Client().post('/user/signup', json.dumps(test), content_type='applications/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message':'DUPLICATE_EMAIL'})
    
    def test_user_signup_password_check(self):
        test        = {'email':'testpy03@gmail.com', 'password':'123456', 'mobile_number':'01055443322'}
        response    = Client().post('/user/signup', json.dumps(test), content_type='applications/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'INVALID_PASSWORD'})
    
    def test_user_signup_except_check(self):
        test        = {'name':'testpy04@gmail.com', 'password':'12345678', 'mobile_number':'01066557744'}
        response    = Client().post('/user/signup', json.dumps(test), content_type='applications/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'INVALID_KEYS'})

# SignIn test
    def test_user_signin_check(self):
        test            = {'email':'testpy@gmail.com', 'password':'12345678'}
        response        = Client().post('/user/signin', json.dumps(test), content_type='applications/json')
        access_token    = response.json()['access_token']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{"access_token" : access_token})

    def test_user_signin_email_check(self):
        test            = {'email':'test99@gmail.com', 'password':'12345678'}
        response        = Client().post('/user/signin', json.dumps(test), content_type='applications/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'INVALID_USER'})

    def test_user_signin_password_check(self):
        test            = {'email':'testpy@gmail.com', 'password':'87654321'}
        response        = Client().post('/user/signin', json.dumps(test), content_type='applications/json') 
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message':'INVALID_PASSWORD'})

    def test_user_signin_except_check(self):
        test            = {'Email':'testpy@gmail.com', 'password':'87654321'}
        response        = Client().post('/user/signin', json.dumps(test), content_type='applications/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'INVALID_KEYS'})

# Myprofile test
class MyprofileTest(TestCase):
    def setUp(self):

        hashed_password = bcrypt.hashpw(('12345678').encode('utf-8'),bcrypt.gensalt())              
        User.objects.create(
            id                  = '1',
            email               ='profiletest@gmail.com',
            password            = hashed_password,
            name                = "test",
            introduction        = "hello my name is test",
            website             = "http://test.com",
            location            = "Republic of Korea",
            twitter             = "@test",
            image               = "test.jpg",
            mobile_number       = "01022334455",
            first_name          = "test",
            last_name           = "pang",
            address             = "seoul",
            zipcode             = "05999"
        )

    def tearDown(self):
        User.objects.filter(email='profiletest@gmail.com').delete()

    def testToken(self):
        test            = {'email':'profiletest@gmail.com', 'password':'12345678'}
        response        = Client().post('/user/signin', json.dumps(test), content_type='applications/json')
        access_token    = response.json()['access_token']
        return access_token

    invalid_token = 'egJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6OTl9.LZJTUoOJr__JN8VvWGE57mQtmWoJwBdMB1-SKGSJHMc'

# get myprofile
    def test_get_myprofile_success(self):
        test_token = self.testToken()
        response = Client().get("/user/myprofile", **{"HTTP_AUTHORIZATION":test_token,"content_type" : "application/json"})
        self.assertEqual(response.status_code, 200)

    def test_get_myprofie_fail(self):
        response = Client().get("/user/myprofile", **{"HTTP_AUTHORIZATION":self.invalid_token,"content_type" : "application/json"})
        self.assertEqual(response.status_code, 401,{'message' : 'INVALID_TOKEN'})

# post MyprofileEdit
    def test_post_myprofile_edit(self):
        test_token = self.testToken()
        test = {
            'name'      : 'edit_test',
            'email'     : 'edit_test@gmail.com',
            'bio'       : 'edit_test',
            'website'   : 'http://edit.com',
            'location'  : 'South Korea',
            'twitter'   : '@edit_test',
            'images'    : 'edit_test.png'
        }
        response        = Client().post('/user/myprofile-edit', json.dumps(test), **{"HTTP_AUTHORIZATION":test_token,"content_type" : "application/json"})
        self.assertEqual(response.status_code, 200)

    def test_post_myprofile_edit_fail(self):
        test_token = self.testToken()
        test = {
            'mobile_number'  : '01032429999',
            'mail'           : 'edit_test@gmail.com',
            'bio'            : 'edit_test',
            'website'        : 'http://edit.com',
            'location'       : 'South Korea',
            'twitter'        : '@edit_test',
            'images'         : 'edit_test.png'
        }
        response        = Client().post('/user/myprofile-edit', json.dumps(test), **{"HTTP_AUTHORIZATION":test_token,"content_type" : "application/json"})
        self.assertEqual(response.status_code, 400, {'message':'INVALID_USER'})

    def test_post_myprofile_edit_except(self):
        test_token = self.testToken()
        test = {
            'fullname'  : 'edit_test',
            'email'     : 'edit_test@gmail.com',
            'bio'       : 'edit_test',
            'website'   : 'http://edit.com',
            'location'  : 'South Korea',
            'twitter'   : '@edit_test',
            'images'    : 'edit_test.png'
        }
        response        = Client().post('/user/myprofile-edit', json.dumps(test), **{"HTTP_AUTHORIZATION":test_token,"content_type" : "application/json"})
        self.assertEqual(response.status_code, 400, {'message':'INVALID_KEYS'})

# post MyShippingAddressEdit
    def test_post_myshippingaddress_edit(self):
        test_token = self.testToken()
        test = {
            'first_name'    : 'first_test',
            'last_name'     : 'laset_test',
            'address'       : 'address_test',
            'zipcode'       : '05999',
            'mobile_number' : "01022334422"
        }
        response        = Client().post('/user/myshippingaddress-edit', json.dumps(test), **{"HTTP_AUTHORIZATION":test_token,"content_type" : "application/json"})
        self.assertEqual(response.status_code, 200)

    def test_post_myshippingaddress_edit_fail(self):
        test_token = self.testToken()
        test = {
            'mobile_number'  : '01032429999',
            'first_name'     : 'first_test',
            'last_name'      : 'laset_test',
            'address'        : 'address_test'
        }
        response        = Client().post('/user/myshippingaddress-edit', json.dumps(test), **{"HTTP_AUTHORIZATION":test_token,"content_type" : "application/json"})
        self.assertEqual(response.status_code, 400, {'message':'INVALID_USER'})

    def test_post_myshippingaddress_edit_except(self):
        test_token = self.testToken()
        test = {
            'Fulltname' : 'first_test',
            'last_name'  : 'laset_test',
            'address'   : 'address_test',
            'zip_code'   : '05999'
        }
        response        = Client().post('/user/myshippingaddress-edit', json.dumps(test), **{"HTTP_AUTHORIZATION":test_token,"content_type" : "application/json"})
        self.assertEqual(response.status_code, 400, {'message':'INVALID_KEYS'})