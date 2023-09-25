import email
from pyexpat import model
from rest_framework import serializers
from photo.models import Photo,category
from django.contrib.auth.models import User

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email']

class photoSerializer(serializers.ModelSerializer):
    category = categorySerializer(many=False)
    user = UserSerializer(many = False)
    class Meta:
        model = Photo
        fields = '__all__'