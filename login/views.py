from django.shortcuts import render
from .serializers import UserSerializer, ProfileSerializer, LoginSerializer# , MyTokenObtainPairSerializer
from .models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly 
                               # all methods need Authenticate  # => GET method 허용시 사용
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.contrib.auth import login, logout, authenticate
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.views import TokenObtainPairView


# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer

class BlacklistRefreshView(APIView):   # 로그아웃시 리프레시 토큰 blacklist
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Success")
    
class HelloView(APIView):       # just for test
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

# 회원가입
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileList(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    #authentication_classes = [SessionAuthentication]
    #permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = ProfileSerializer

# class LoginView(generics.GenericAPIView):
#     serializer_class = LoginSerializer

#     def post(self, request): 
#         user = User.objects.get(email=request.data['email'])
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         token = serializer.validated_data
#         login(request, user)
#         return Response({
#             'id': user.id,
#             'email': user.email,
#             'name': user.name,
#             'token': token.key,},
#             status=status.HTTP_200_OK)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.get(email=request.data['email'])
        # user = authenticate(request, username=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            serializer = ProfileSerializer(user)
            return Response({
                'id': serializer.data.get('id'),
                'email': serializer.data.get('email'),
                'name': serializer.data.get('name'),
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
# class LogoutView(APIView):
#     def get(self, request, format=None):
#         # using Django logout
#         logout(request)
#         return Response(status=status.HTTP_200_OK)