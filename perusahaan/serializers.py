from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import users,company

# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']
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
    users = UserProfileSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id','url', 'username','email','users','company']


# class UserSerializer(serializers.ModelSerializer):
#     users = serializers.PrimaryKeyRelatedField(many=True,queryset=users.objects.all())
#     class Meta:
#         model = User
#         fields = ['id', 'username','users']
