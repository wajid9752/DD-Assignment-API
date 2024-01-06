from rest_framework import serializers
from account.models import User
from manager.models import *


class AddProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "start_date",
            "end_date"
        ]



class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  
        fields = ['username', 'email']


class TeamViewSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)
    project=serializers.SerializerMethodField()

    def get_project(self,obj):
        return obj.project.name

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "project",
            "members"
        ]

class TeamAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['project','name', 'members']


class TeamSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)

    class Meta:
        model = Team
        fields = ['name', 'manager', 'members']





class ProjectViewSerializer(serializers.ModelSerializer):
    team_working = serializers.SerializerMethodField()

    def get_team_working(self, obj):
        teams = obj.teamProjects.all()
        return TeamSerializer(teams, many=True).data

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "start_date",
            "end_date",
            "team_working"
        ]



class ProjectStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['is_completed']


#########  TASK 
class AssignTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "deadline",
            "priority",
            "status",
            "assigned_to",
            "project"
        ] 