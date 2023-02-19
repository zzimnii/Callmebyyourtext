from django.shortcuts import render
from .serializers import UserSerializer, ProfileSerializer, LoginSerializer
from .models import User
from rest_framework import generics, status
from rest_framework.response import Response

# 회원가입
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileList(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data
        return Response({
            'token': token.key,},
            status=status.HTTP_200_OK)