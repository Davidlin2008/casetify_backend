import json
import bcrypt


from django.test    import TestCase
from django.test    import Client 
from datetime       import datetime
from unittest.mock  import patch, MagicMock

from .models        import User

class UserTest(TestCase):
    def setUp(self): 

        hashed_password = bcrypt.hashpw(('12345678').encode('utf-8'),bcrypt.gensalt())              
        User.objects.create(
            email='testpy@gmail.com',
            password= hashed_password.decode('UTF-8'),
            phone_number='01012345678'
        )

    def tearDown(self):
        User.objects.filter(email='testpy@gmail.com').delete()

# SignUp test
    def test_user_signup_check(self):
        test        = {'email': 'testpy01@gmail.com', 'password':'12345678', 'phone_number':'01011223344'}
        response    = Client().post('/user/signup', json.dumps(test), content_type='applications/json')
        self.assertEqual(response.status_code, 200)
    
    def test_user_signup_email_check(self):
        test        = {'email':'testpy@gmail.com', 'password':'12345678', 'phone_number':'01044332211'}
        response    = Client().post('/user/signup', json.dumps(test), content_type='applications/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message':'DUPLICATE_EMAIL'})
    
    def test_user_signup_password_check(self):
        test        = {'email':'test02@gmail.com', 'password':'123456', 'phone_number':'01055443322'}
        response    = Client().post('/user/signup', json.dumps(test), content_type='applications/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'INVALID_PASSWORD'})
    
    def test_user_signup_except_check(self):
        test        = {'name':'test03@gmail.com', 'password':'12345678', 'phone_number':'01066557744'}
        response    = Client().post('/user/signup', json.dumps(test), content_type='applications/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'INVALID_KEYS'})

# SignIn test
    def test_user_signin_check(self):
        test        = {'email':'testpy@gmail.com', 'password':'12345678'}
        response    = Client().post('/user/signin', json.dumps(test), content_type='applications/json')
        access_token = response.json()['access_token']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{"access_token" : access_token})

    def test_user_signin_email_check(self):
        test        = {'email':'test99@gmail.com', 'password':'12345678'}
        response    = Client().post('/user/signin', json.dumps(test), content_type='applications/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'INVALID_USER'})

    def test_user_signin_password_check(self):
        test        = {'email':'testpy@gmail.com', 'password':'87654321'}
        response    = Client().post('/user/signin', json.dumps(test), content_type='applications/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message':'INVALID_PASSWORD'})

    def test_user_signin_except_check(self):
        test        = {'Email':'testpy@gmail.com', 'password':'87654321'}
        response    = Client().post('/user/signin', json.dumps(test), content_type='applications/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'INVALID_KEYS'})