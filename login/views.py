from django.shortcuts import render
from .serializers import UserSerializer, ProfileSerializer
from .models import User
from rest_framework import generics

# 회원가입
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer