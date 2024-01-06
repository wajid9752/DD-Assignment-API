from imports import *
from rest_framework import generics

# Token 5b269f6a6e9d47c8a2ddcc9d47cf82682d243431
# Token f270e8cdb652d24d1acd816f0c0f379996b9920f


class IsManagerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'manager'


class ManagerHomeAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsManagerUser]

    def get(self, request, *args, **kwargs):

        project_stats = Project.objects.aggregate(
            total_completed_projects=Count('id', filter=models.Q(is_completed=True)),
            total_active_projects=Count('id', filter=models.Q(is_completed=False)),
        )
        
        my_team = TeamViewSerializer(
            Team.objects.filter(manager=request.user),
            many=True
        ).data
        
        projects = ProjectSerializer(
            Project.objects.filter(manager=request.user).order_by('-created_at') ,
            many=True
        )

        data = {
           'total_completed_projects': project_stats['total_completed_projects'],
           'total_active_projects': project_stats['total_active_projects'],
           'projects': projects.data,
           'teams': my_team , 
        }
        return Response(data, status=status.HTTP_200_OK)



class AddProjectAPIView(generics.RetrieveUpdateAPIView, generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = AddProjectSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsManagerUser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProjectViewSerializer
        elif self.request.method == 'PATCH':
            return ProjectStatusSerializer
        else:
            return AddProjectSerializer

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)

    def perform_update(self, serializer):
        serializer.save(manager=self.request.user)

    def perform_partial_update(self, serializer):
        serializer.save(manager=self.request.user)

##############  TEAMM  
@api_view(['POST'])
@authentication_classes([TokenAuthentication]) 
@permission_classes([IsAuthenticated , IsManagerUser])  
def add_team(request):
    try:
        data = request.data 
        serializer = TeamAddSerializer(data=data)
        if serializer.is_valid():
            serializer.save(manager=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

############### TASK Assigned
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication]) 
@permission_classes([IsAuthenticated , IsManagerUser])  
def assign_task(request):
    try:
        data = request.data 
        serializer = AssignTaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
