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

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        if len(data['password']) < 8:
            return JsonResponse({'message':'INVALID_PASSWORD'}, status=400)
        if len(data['phone_number']) != 11:
            return JsonResponse({'message':'INVALID_PHONE_NUMBER'}, status=400)
        try:
            validate_email(data['email'])
            
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'DUPLICATE_EMAIL'}, status=401)
            if User.objects.filter(phone_number=data['phone_number']).exists():
                return JsonResponse({'message':'DUPLICATE_PHONE_NUMBER'}, status=401)

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt())              
            User(
                email           = data['email'],
                password        = hashed_password.decode('utf-8'),
                phone_number    = data['phone_number']
            ).save()
            return HttpResponse(status=200)

        except ValidationError:
            return JsonResponse({'message':'INVALID_EMAIL_SYNTAX'}, status=400) 
        except TypeError:
            return JsonResponse({'message':'FAILED_HASHED'}, status=400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status=400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            user = User.objects.get(email = data['email'])
            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({'id':user.id},SECRET_KEY,algorithm='HS256') 
                return JsonResponse({'access_token':access_token.decode('utf-8')}, status = 200)
            else:
                return JsonResponse({'message':'INVALID_PASSWORD'}, status = 401)
                        
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status = 400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status = 400)