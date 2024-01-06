from imports import *


class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        data=UserSerializer(user).data
        return Response(data, status=status.HTTP_200_OK)

    