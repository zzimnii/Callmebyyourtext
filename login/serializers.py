from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # user = User.objects.create_user(
        #     email = validated_data['email'],
        #     nickname = validated_data['nickname'],
        #     name = validated_data['name'],
        #     password = validated_data['password'],
        #     point = validated_data['point']
        # )
        # return user
        user = User.objects.create_user(
            email = validated_data.get('email'),
            nickname = validated_data.get('nickname'),
            name = validated_data.get('name'),
            password = validated_data.get('password'),
            point = 500
        )
        return user
    
    class Meta:
        model = User
        fields = ['name', 'nickname', 'email', 'password'] # 회원 가입시에는 point 항목이 보이지 않지만
                                                                    # 회원 detail에는 point 항목이 보이게 하고싶다.
class UserPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'nickname', 'email', 'password', 'point']