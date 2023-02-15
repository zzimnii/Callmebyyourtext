from django.shortcuts import render
from .serializers import UserSerializer, UserPageSerializer
from .models import User
from rest_framework import generics

# 회원가입
class UserCreate(generics.ListCreateAPIView):   # 회원 생성
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):    # 회원 detail(수정, 삭제)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserPage(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserPageSerializer