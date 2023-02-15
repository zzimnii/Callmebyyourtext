# from .models import User
# from rest_framework import serializers
# from rest_framework.validators import UniqueValidator
# from django.contrib.auth.password_validation import validate_password
# from rest_framework.authtoken.models import Token

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