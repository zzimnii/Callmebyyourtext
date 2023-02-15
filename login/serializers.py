# from .models import User
# from rest_framework import serializers
# from rest_framework.validators import UniqueValidator
# from django.contrib.auth.password_validation import validate_password
# from rest_framework.authtoken.models import Token
# from django.contrib.auth import authenticate

# class UserPageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['name', 'nickname', 'email', 'password', 'point']

# class UserSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#         required=True,
#         validators=[UniqueValidator(queryset=User.objects.all())],
#     )
#     password = serializers.CharField(
#         write_only = True,
#         required=True,
#         validators=[validate_password],
#     )
#     password2 = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model=User
#         fields=['email', 'name', 'nickname', 'password', 'password2', ]

#     def validate(self, data):
#         if data['password'] != data['password2']:
#             raise serializers.ValidationError(
#                 {"password": "Password fields didn't match"})

#         return data

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             nickname=validated_data['nickname'],
#             email=validated_data['email'],
#             name=validated_data['name'],
#             point=500
#         )

#         user.set_password(validated_data['password'])
#         user.save()
#         # token = Token.objects.create(user=user)
#         return user

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
 
# User Serializer
# 유저(사용자) 시리얼라이저는 간단하기도하고 Delete serializer와도 매우 유사합니다.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
 
# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwards = {'password': {'write_only': True}}
 
    def create(self, validated_data):
        user = User.objects.create_user(validated_data
        ['username'], validated_data['email'], validated_data['password'])
 
        return user
 
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
 
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")