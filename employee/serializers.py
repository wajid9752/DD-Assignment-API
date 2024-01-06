from rest_framework import serializers
from account.models import User
from manager.models import *


class MyTaskSerializer(serializers.ModelSerializer):
    project=serializers.SerializerMethodField()
    manager=serializers.SerializerMethodField()
    
    def get_project(self,obj):
        return obj.project.name
    
    def get_manager(self,obj):
        return obj.project.manager.username
    
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "deadline",
            "priority",
            "status",
            "project",
            "manager",
        ] 

class UpdateTaskStatus(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [ "status"]         