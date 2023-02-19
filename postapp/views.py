from .models import Question, Comment
from login.models import User
# from django.contrib.auth.models import User, AbstractUser
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
    #authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsOwnerOrReadOnly]    #비로그인 유저도 작성창은 나옴

    def get_serializer_class(self):
        writer = self.request.user
        if self.action == 'list':
            return CommentSerializer
        if self.action == 'retrieve':
            # print(User.point)
            return CommentSerializer
        if self.action == 'create':
            if writer.is_anonymous:      #비로그인 유저인것까지는 판별0 -> AnonymousUser인것을 User로 바꾸던지 writer를 Anonymous로 바꿔야함..
                print(writer)
                # writer = NULL
                # isinstance(self.request.user, User)
            # print(User.point)
            # User.point += 50
            return CommentCreateSerializer
        return CommentCreateSerializer

    def perform_create(self, serializer):
        if self.request.user.id == None:
            # handles anonymous users
            serializer.save(writer=self.request.user.id)
        else:
            serializer.save(writer=self.request.user)

    def get_queryset(self, **kwargs): # Override
        question_id = self.kwargs['question_id']
        return self.queryset.filter(question=question_id)
