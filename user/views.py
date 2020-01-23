import jwt
import json
import bcrypt
import requests

from django.views               import View
from django.http                import JsonResponse, HttpResponse
from django.db                  import IntegrityError
from casetify_backend.settings  import SECRET_KEY
from django.core.validators     import validate_email
from django.core.exceptions     import ValidationError

from .models                    import User
from .utils                     import login_decorator

class SignUpView(View):
    def validate_input(self, data):

        if len(data['password']) < 8:
            return JsonResponse({'message':'INVALID_PASSWORD'}, status=400)
       
        if User.objects.filter(email=data['email']).exists():
            return JsonResponse({'message':'DUPLICATE_EMAIL'}, status=401)
        
        return None

    def post(self, request):
        data = json.loads(request.body)
        
        try:
            validate_email(data['email'])
            validation = self.validate_input(data)
       
            if validation: return validation

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt())              
            User(
                email           = data['email'],
                password        = hashed_password,
                mobile_number    = data['mobile_number']
            ).save()
            return HttpResponse(status=200)

        except ValidationError:
            return JsonResponse({'message':'INVALID_EMAIL_SYNTAX'}, status=400)
        except TypeError:
            return JsonResponse({'message':'INVALID_TYPE'}, status=400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status=400)
        
class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            user = User.objects.get(email = data['email'])
        
            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({'id':user.id},SECRET_KEY,algorithm='HS256') 
                return JsonResponse({'access_token':access_token.decode('utf-8')}, status=200)

            return JsonResponse({'message':'INVALID_PASSWORD'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=400)   
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status=400)

class MyprofileView(View):
    @login_decorator
    def get(self,request):
        
        try:
            user = User.objects.get(id=request.user.id)
            result = {
                "name"          : user.name,
                "email"         : user.email,
                "bio"           : user.introduction,
                "website"       : user.website,
                "location"      : user.location,
                "twitter"       : user.twitter,
                "images"        : user.image,
                "mobile_number" : user.mobile_number,
                "first_name"    : user.first_name,
                "last_name"     : user.last_name,
                "address"       : user.address,
                "zipcode"       : user.zipcode
            }

            return JsonResponse(result, status=200)
        
        except user.DoesNotExist:
            return JsonResponse({"message":"INVALID_USER"}, status=400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status=400)

class MyprofileEditView(View):
    @login_decorator
    def post(self,request):
        data = json.loads(request.body)
        user = User.objects.get(id=request.user.id)
        try:    
            
            user.name            = data['name']
            user.email           = data['email']
            user.introduction    = data['bio']
            user.website         = data['website']
            user.location        = data['location']
            user.twitter         = data['twitter']
            user.image           = data['images']
            user.save()

            return HttpResponse(status=200)
        
        except user.DoesNotExist:
            return JsonResponse({"message":"INVALID_USER"}, status=400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status=400)

class MyShippingAddressEditView(View):
    @login_decorator
    def post(self,request):
        data = json.loads(request.body)
        user = User.objects.get(id=request.user.id)
        try:
            
            user.first_name     = data['first_name']
            user.last_name      = data['last_name']
            user.address        = data['address']
            user.zipcode        = data['zipcode']
            user.mobile_number  = data['mobile_number']
            user.save()
            
            return HttpResponse(status=200)
        
        except user.DoesNotExist:
            return JsonResponse({"message":"INVALID_USER"}, status=400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status=400)


class KakaologinView(View):
    def post(self, request):
        try:
            kakao_token = request.headers["Authorization"]
            print('kt',kakao_token)
            headers = ({"Authorization": f"Bearer {kakao_token}"})
            url = "https://kapi.kakao.com/v1/user/me"
            response = requests.get(url, headers=headers)
            print('kakao re',response.json)
            kakao_user = response.json()
            print(kakao_user)

        except KeyError:
            return JsonResponse({"message" : "INVALID_TOKEN"}, status = 400)
        except kakao_token.DoesNotExist:
            return JsonResponse({'message':'INVALID_TOKEN'}, status=400)
        
        if User.objects.filter(kakao_id=kakao_user["id"]).exists():
            user_id = User.objects.get(kakao_id=kakao_user["id"]).id
            print('user_id',user_id)
            access_token = jwt.encode({'id':user_id}, SECRET_KEY, algorithm="HS256")
            print('access_token', access_token)
            return JsonResponse({"access_token" : access_token.decode('utf-8')}, status = 200)
            
        else:
            newUser = User.objects.create(
                kakao_id    = kakao_user["id"],
                email       = kakao_user["kaccount_email"], 
                name        = kakao_user["properties"]["nickname"]
            )
            access_token = jwt.encode({'id': newUser.id}, SECRET_KEY, algorithm="HS256")
            return JsonResponse({"access_token": access_token.decode('utf-8')}, status = 200)