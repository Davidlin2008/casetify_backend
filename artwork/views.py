import jwt
import json

#from user.models import *
#from user.utils  import login_decorator
from .models      import *

from django.views     import View
from django.http      import JsonResponse, HttpResponse, HttpRequest
from django.db        import IntegrityError
from django.db.models import Avg
from django.db.models import Q

class HahaView(View):
    def post(self, request):
        temp = json.loads(request.body)
        print(temp['data'])

        return HttpResponse(status=200)

    def get(self, request):
        return JsonResponse({'message':'haha'}, status=200)



class RegularArtworkListView(View):
    def get(self, request):
        offset    = int(request.GET['offset'])
        limit     = int(request.GET['limit'])
        
        result = []
        artwork = ArtworkPrice.objects.select_related('artwork','device').filter(artwork__is_customed=False)[offset:limit]
        #i.artwork.regularartworkimage_set.filter(artwork_id=i.artwork.id).values('image_1')
        
        for i in artwork:
            #print(i.artwork.id, i.device.name, i.artwork.artwork_type.name, i.artwork.name, i.price) 
            #print(i.artwork.id)
            artwork_images = list(i.artwork.regularartworkimage_set.filter(artwork_id=i.artwork.id, device_color_id=1).values('image_1'))
            print(artwork_images)
            image_list    = list(i.artwork
                                 .regularartworkimage_set
                                 .filter(artwork_id=i.artwork.id)
                                 .values('artwork_color__id','artwork_color__name','artwork_color__info')
                                 .distinct())
            for j in range(0,len(image_list)):
                image_list[j]['src'] = artwork_images[j]['image_1']

            temp = []
            for k in image_list:
                a = {}
                a['id'] = k['artwork_color__id']
                if "border" in k['artwork_color__info']:
                    a['border'] = k['artwork_color__info']
                elif "http" in k['artwork_color__info']:
                    a['image'] = k['artwork_color__info']
                else:
                    a['color'] = k['artwork_color__info']

                a['src'] = k['src']

                temp.append(a)

            result.append({"id"         : i.artwork.id,
                           "model"      : (i.device.name+i.artwork.artwork_type.name),
                           "name" : i.artwork.name,
                           "price"      : i.price,
                           "image"      : temp
                          })

        return JsonResponse({'item':result}, status = 200)



