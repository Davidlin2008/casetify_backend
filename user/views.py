import jwt
import json
import bcrypt

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

        if len(data['mobile_number']) != 11:
            return JsonResponse({'message':'INVALID_PHONE_NUMBER'}, status=400)
        
        if User.objects.filter(email=data['email']).exists():
            return JsonResponse({'message':'DUPLICATE_EMAIL'}, status=401)
                
        if User.objects.filter(mobile_number=data['mobile_number']).exists():
            return JsonResponse({'message':'DUPLICATE_MOBLIE_NUMBER'}, status=401)
        
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
                password        = hashed_password.decode('utf-8'),
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
                "Name"          : user.nick_name,
                "Mail"          : user.email,
                "Bio"           : user.introduction,
                "Website"       : user.website,
                "Location"      : user.location,
                "Twitter"       : user.twitter,
                "Images"        : user.image,
                "Phone_number"  : user.mobile_number,
                "Firstname"     : user.first_name,
                "Lastname"      : user.last_name,
                "Address"       : user.address,
                "Zipcode"      : user.zipcode
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

        try:    
            user = User.objects.get(id=request.user.id)
            user.nick_name       = data['Name']
            user.email           = data['Mail']
            user.introduction    = data['Bio']
            user.website         = data['Website']
            user.location        = data['Location']
            user.twitter         = data['Twitter']
            user.image           = data['Images']
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
        
        try:
            user = User.objects.get(id=request.user.id)

            user.first_name  = data['Firstname']
            user.last_name   = data['Lastname']
            user.address     = data['Address']
            user.zipcode     = data['Zipcode']
            user.save()
            
            return HttpResponse(status=200)
        
        except user.DoesNotExist:
            return JsonResponse({"message":"INVALID_USER"}, status=400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status=400)