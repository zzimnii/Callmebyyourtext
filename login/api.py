from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from django.contrib.auth.models import User
 
# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
 
## kwargs basically means it can take more arguments
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save() 
        # 위의 save 코드로 인해 data가 저장됨
        return Response({
            "user": UserSerializer(user,
            context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })
 
# Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        # 위의 validated_data로써 계정 인증을 
        return Response({
            "user": UserSerializer(user,
            context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })
 
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer
 
    def get_object(self):
        return self.request.user
