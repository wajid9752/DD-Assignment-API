from imports import *


# 3a0a3e237a75e230aa4f2e1aac3708195ab7bfca
class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'


class AdminHomeAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]

    def get(self, request, *args, **kwargs):

        project_stats = Project.objects.aggregate(
            total_completed_projects=Count('id', filter=models.Q(is_completed=True)),
            total_active_projects=Count('id', filter=models.Q(is_completed=False)),
        )
        
        employees = AdminViewUser(
                            User.objects.filter(role__in=['employee', 'manager']) ,
                            many=True)
        
        projects = ProjectSerializer(
            Project.objects.all().order_by('-created_at') ,
            many=True
        )

        data = {
            'total_employees': User.objects.filter(role__in=['employee', 'manager']).count(),
            'employees': employees.data ,
           'total_completed_projects': project_stats['total_completed_projects'],
           'total_active_projects': project_stats['total_active_projects'],
           'projects': projects.data
        }

        return Response(data, status=status.HTTP_200_OK)
    

class AddEmployeeAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]

    def post(self, request, *args, **kwargs):
        try:
            serializer = AddUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data , status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors , status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
        


@api_view(['PATCH'])
@authentication_classes([TokenAuthentication]) 
@permission_classes([IsAuthenticated , IsAdminUser])  
def update_user_status(request, pk):
    try:
        obj = User.objects.get(id=pk)
        data = request.data

        if 'active' not in data:
            return Response({"active": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserStatusUpdate(data=data, instance=obj, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@api_view(['GET'])
@authentication_classes([TokenAuthentication]) 
@permission_classes([IsAuthenticated , IsAdminUser])  
def filter_user(request):
    try:
        _status = request.data.get('status')
        serializer =  UserSerializer(
                            User.objects.filter(role__in=['employee', 'manager'] , active=bool(_status)) ,
                            many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        