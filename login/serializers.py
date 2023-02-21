from .models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from datetime import datetime

class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ("email", "name", "password", "password2")
    
    def validate(self, data):
        if data['password']!= data['password2']:
            raise serializers.ValidationError(
                {"password": "Passwords don't match."})
        
        return data
    
    def create(self, validated_data):
        x = datetime.now()
        user = User.objects.create_user(
            id = str(x.year)+str(x.month)+str(x.day)+str(x.hour)+str(x.minute)+str(x.second)+str(x.microsecond),
            name=validated_data['name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user
    
class ProfileSerializer(serializers.ModelSerializer): # 전체 유저 정보 조회
    class Meta:
        model = User
        fields = ['email', 'name', 'point']

class LoginSerializer(serializers.Serializer):  # 회원가입한 유저 로그인 
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user)
            return token
        raise serializers.ValidationError(
            {"error":"Unable to log in with provided credentials."})

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['point']
    def update(self, instance, validated_data):
        instance.point = validated_data.get('point', instance.point)
        instance.save()
        return instance  