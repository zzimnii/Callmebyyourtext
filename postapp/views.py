from .models import Question, Comment
from login.models import User
from login.serializers import PointSerializer
from .serializers import QuestionSerializer, QuestionDetailSerializer, CommentSerializer, CommentCreateSerializer
from login.serializers import LoginSerializer
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .permissions import IsOwnerOrReadOnly

class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all().order_by('-created_at')
    serializer_class = QuestionSerializer
    #authentication_classes = [BasicAuthentication, SessionAuthentication]
    authentication_classes = [TokenAuthentication]
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
        if self.request.user.id == None:
            serializer.save(writer=self.request.user.id)
        else:
            serializer.save(writer = self.request.user)


class QuestionListSet(ModelViewSet):
    queryset = Question.objects.all().order_by('-created_at')
    serializer_class = QuestionSerializer
    def get_queryset(self, **kwargs): # Override
        writer = self.kwargs['writer']
        return self.queryset.filter(writer=writer)
    def get_serializer_class(self):
        if self.action == "create":
            return CommentCreateSerializer
        


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    permission_classes = [IsOwnerOrReadOnly]
    def get_serializer_class(self): 
        writer = self.request.user
        if self.action == 'list':
            return CommentSerializer
        if self.action == 'retrieve':
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
        
    def retrieve(self, request, pk=None, **kwargs):
        question_id = self.kwargs['question_id']
        question = get_object_or_404(Question, id=question_id)
        print(question.writer.id)   #질문 작성자 ID
        if self.request.user.id != None:             #로그인 했을때
            comment = Comment.objects.all()
            comment = get_object_or_404(Comment, pk=pk)
            if comment.open_user.filter(id=request.user.id).exists():
                print('이미 열어본 답변')
                serializer=CommentSerializer(comment)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                print('처음 열어보는 답변')
                comment.open_user.add(request.user)
                loginUser = request.user
                if loginUser.id == question.writer.id:
                    loginUser.point -= 50
                else:
                    print('-100')
                    loginUser.point -= 100
                update_serial=PointSerializer(loginUser, data=request.data, partial=True)
                if update_serial.is_valid():
                    update_serial.save()
                    serializer=CommentSerializer(comment)
                return Response(serializer.data, status=status.HTTP_200_OK)
        #로그인 안했을때 어떻게 해야할지?!?!
        else:
            print('로그인후 이용해주세요')
            serializer=LoginSerializer()
        return Response(serializer.data, status=status.HTTP_401_UNAUTHORIZED)
        
    def get_queryset(self, **kwargs): # Override
        question_id = self.kwargs['question_id']
        return self.queryset.filter(questionId=question_id)
