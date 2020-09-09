from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import users,company,presence
from django.contrib.auth.hashers import make_password

# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']

class PresenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = presence
        fields = ['url','id','id_user','id_company','date_presence','start_presence','end_presence']
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = ['id_company','name','telp','profile_pic','start_work','end_work','location','record_location']

class UsersLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = ['id','id_company','location','record_location']
        read_only_fields = ['id_company']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = company
        fields = ['id','start_work','end_work']


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedRelatedField(view_name = 'user-detail',read_only=True)
    users = UserProfileSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id','url','password','username','email','users','company']
    validate_password = make_password