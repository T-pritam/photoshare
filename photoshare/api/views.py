from urllib import response
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import photoSerializer
from photo.models import Photo

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getPhotos(request): 
    photo = Photo.objects.all()
    serializer = photoSerializer(photo,many = True)
    return Response(serializer.data)

@api_view(['POST'])
def getPhoto(request,pk):
    photo = Photo.objects.get(id=pk)    
    serializer = photoSerializer(photo,many = False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review(request,pk):
    photo = Photo.objects.get(id=pk)
    data =  request.data
    print(data)
    r = Photo.objects.get(id = pk)
    r.review = r.review + int(data['value'])
    r.save()
    Photo.save
    serializer = photoSerializer(photo,many = False)
    return Response(serializer.data)