from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import users

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


class UserSerializer(serializers.ModelSerializer):
    users = UserProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id','url', 'username','email','users']


# class UserSerializer(serializers.ModelSerializer):
#     users = serializers.PrimaryKeyRelatedField(many=True,queryset=users.objects.all())
#     class Meta:
#         model = User
#         fields = ['id', 'username','users']
