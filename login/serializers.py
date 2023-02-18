from .models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer): # 유저 생성 
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            password = validated_data['password'],
            nickname = validated_data['nickname']
        )
        token = Token.objects.create(user=user)
        return user
    class Meta:
        model = User
        fields = ['email', 'name', 'nickname', 'password']

class ProfileSerializer(serializers.ModelSerializer): # 전체 유저 정보 조회
    class Meta:
        model = User
        fields = '__all__'

class LoginSerializer(serializers.Serializer):  # 회원가입한 유저 로그인 
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validation(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user)
            return token
        raise serializers.ValidationError(
            {"error":"Unable to log in with provided credentials."})