from rest_framework import serializers
from account.models import User
from manager.models import *



class UserStatusUpdate(serializers.ModelSerializer):
    class Meta:
        model = User  
        fields = ['active']


class AdminViewUser(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email','role','active')

 
        
class ProjectSerializer(serializers.ModelSerializer):
    manager = serializers.SerializerMethodField()

    def get_manager(self,obj):
        return f"{obj.manager.username} - {obj.manager.email}"
    class Meta:
        model = Project
        fields = '__all__'


class AddUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'mobile', 'role', 'password']

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            mobile=validated_data['mobile'],
            username=validated_data['username'],
            role=validated_data['role'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
