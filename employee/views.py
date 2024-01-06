from imports import *

class IsEmployeeUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'employee'

class EmployeeHomeAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsEmployeeUser]

    def get(self, request, *args, **kwargs):
        my_tasks = MyTaskSerializer(
            Task.objects.filter(assigned_to=request.user),
            many=True
        ).data
        

        data = {
           'total_completed_tasks': Task.objects.filter(assigned_to=request.user , status="Completed").count(),
           'total_active_tasks': Task.objects.filter(assigned_to=request.user , status="Pending").count(),
           'tasks': my_tasks , 
        }
        return Response(data, status=status.HTTP_200_OK)
    

@api_view(['PATCH'])
@authentication_classes([TokenAuthentication]) 
@permission_classes([IsAuthenticated , IsEmployeeUser])  
def update_task_status(request, pk):
    try:
        obj = Task.objects.get(id=pk)
        data = request.data

        if 'status' not in data:
            return Response({"status": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UpdateTaskStatus(data=data, instance=obj, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
@authentication_classes([TokenAuthentication]) 
@permission_classes([IsAuthenticated , IsEmployeeUser])  
def filter_task(request):
    try:
        priority = request.data.get('priority')
        _status = request.data.get('status')

        objs = Task.objects.filter(assigned_to=request.user)

        if _status:
            objs = objs.filter(status=_status)

        if priority:
            objs = objs.filter(priority=priority)

        serializer = MyTaskSerializer(objs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


