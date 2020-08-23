from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import users

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id','url', 'username','email']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = ['id','id_company','latitude_office','longtitude_office']