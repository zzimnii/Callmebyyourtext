from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from django.contrib.auth import authenticate

from .models import Profile

# Username을 받지 않는데 어떻게 항목에 받는지? 단순히 fields에 적어놓는다는 이유로? 
# username에 대한 자료형도 선언하지 않았는데? 또한 ModelSerializer에 username이라는 항목도 없음...
class RegisterSerializer(serializers.ModelSerializer):
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
        fields = ("username", "email", "password", "password2")
    
    def validate(self, data):
        if data['password']!= data['password2']:
            raise serializers.ValidationError(
                {"password": "Passwords don't match."})
        
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user
    # User모델이 만들어질때 username은 unique=False로 만들고싶음
    # 로그아웃또한 구현하고 싶음

    
class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = '__all__'
    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user)
            return token
        raise serializers.ValidationError(
            {"error":"Unable to log in with provided credentials."})
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('point', 'image')
# Profile모델 뿐만 아니라 User모델의 항목도 함께 보여주고 싶음
# => Profile모델에 User모델의 속성을 ForiegnKey를 이용하여 연결한 후
# Profile 모델만 보여주기