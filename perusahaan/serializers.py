from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import users

# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']

class UsersSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField()
    class Meta:
        model = users
        # fields = ['id','id_company','location','user']
        fields = ['id_company','location']


class UserSerializer(serializers.ModelSerializer):
    users = UsersSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id','url', 'username','email','users']


# class UserSerializer(serializers.ModelSerializer):
#     users = serializers.PrimaryKeyRelatedField(many=True,queryset=users.objects.all())
#     class Meta:
#         model = User
#         fields = ['id', 'username','users']
