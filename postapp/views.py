from .models import Question, Comment
from login.models import User
from login.serializers import PointSerializer
from .serializers import QuestionSerializer, QuestionDetailSerializer, CommentSerializer, CommentCreateSerializer
from rest_framework.viewsets import ModelViewSet

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .permissions import IsOwnerOrReadOnly
from django.views.decorators.csrf import csrf_exempt


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    #authentication_classes = [BasicAuthentication, SessionAuthentication]
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == "create":
            return QuestionSerializer
        if self.action == "list":
            return QuestionDetailSerializer
        if self.action == "retrieve":
            return QuestionDetailSerializer
        
        return QuestionSerializer

    def perform_create(self, serializer, **kwargs):
        if self.request.user.id == None:
            print(self.request.user.id)
            print('로그인 안한거')
            #self.request.user.id=None으로 나옴
            serializer.save(writer=self.request.user.id)
        else:
            serializer.save(writer = self.request.user)


class QuestionListSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self, **kwargs): # Override
        writer = self.kwargs['writer']
        if writer==0:
            writer=None
            return self.queryset.filter(writer=None)
        else:
            print('영 아님')
        return self.queryset.filter(writer=writer)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    # authentication_classes = [TokenAuthentication]
    def get_serializer_class(self):
        writer = self.request.user
        if self.action == 'list':
            return CommentSerializer
        if self.action == 'retrieve':
            if self.request.user.id != None:        #로그인 했을때.
                loginUser = self.request.user
                print(loginUser.name)
                loginUser.point -= 50
                print(loginUser.point)
                update_serial=PointSerializer(loginUser, data=self.request.data, partial=True)
                if update_serial.is_valid():
                    update_serial.save()
            return CommentSerializer
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentCreateSerializer

    def perform_create(self, serializer):
        if self.request.user.id == None:
            serializer.save(writer=self.request.user.id)
        else:
            loginUser = self.request.user
            serializer.save(writer=self.request.user)
            loginUser.point += 50
            update_serial=PointSerializer(loginUser, data=self.request.data, partial=True)
            if update_serial.is_valid():
                update_serial.save()
        

    def get_queryset(self, **kwargs): # Override
        question_id = self.kwargs['question_id']
        return self.queryset.filter(question=question_id)


