from .models import Question, Comment
from login.models import User
from login.serializers import UserSerializer
from .serializers import QuestionSerializer, QuestionDetailSerializer, CommentSerializer, CommentCreateSerializer
from rest_framework.viewsets import ModelViewSet

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .permissions import IsOwnerOrReadOnly
from django.views.decorators.csrf import csrf_exempt


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == "create":
            return QuestionSerializer
        if self.action == "list":
            return QuestionDetailSerializer
        if self.action == "retrieve":
            return QuestionDetailSerializer
        
        return QuestionSerializer

    def perform_create(self, serializer, **kwargs):
        serializer.save(writer = self.request.user)

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        writer = self.request.user
        if self.action == 'list':
            return CommentSerializer
        if self.action == 'retrieve':
            # print(User.point)
            return CommentSerializer
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentCreateSerializer

    def perform_create(self, serializer):
        #print(self.request.user)   -> userId가 나옴
        #로그인된 유저를 특정 -> 그 유저의 point에 추가해야댐
        print("포인트 50 추가해줘..")
        if self.request.user.id == None:
            serializer.save(writer=self.request.user.id)
        else:
            loginUser = self.request.user
            # loginUser.point += 50    #프린트는 되는데 DB에 저장X ... 왜????
            print(loginUser)
            loginUser.point += 50
            point = loginUser.point
            print(point)
            serializer.save(writer=self.request.user)
            if UserSerializer.is_valid():
                UserSerializer.save(point)
        

    def get_queryset(self, **kwargs): # Override
        question_id = self.kwargs['question_id']
        return self.queryset.filter(question=question_id)