from .models import Question, Comment, RecQuestion, BeQuestion, BeComment
from login.serializers import PointSerializer
from .serializers import QuestionSerializer, QuestionDetailSerializer, CommentSerializer, CommentCreateSerializer, CommentLikeSerializer, RecQuestionSerializer, BeQuestionSerializer, BeQuestionDetailSerializer, BeCommentCreateSerializer, BeCommentLikeSerializer, BeCommentSerializer
from login.serializers import LoginSerializer
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .permissions import IsOwnerOrReadOnly, IsOwnerBeOrReadOnly
import jwt
from login.models import User
from blossom.settings import JWT_SECRET_KEY
#질문 CRUD
class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all().order_by('-created_at')
    serializer_class = QuestionSerializer
    #authentication_classes = [BasicAuthentication, SessionAuthentication]
    authentication_classes = [TokenAuthentication]
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
        access_token = self.request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        decoded = jwt.decode(access_token, algorithms=['HS256'], verify=True, key=JWT_SECRET_KEY)
        user_id = decoded['user_id']
        writer = User.objects.get(pk=user_id)
        serializer.save(writer=writer)
        # if self.request.user.id == None:
        #     serializer.save(writer=self.request.user.id)
        # else:
        #     serializer.save(writer = self.request.user)

#UserId별 질문 리스트
class QuestionListSet(ModelViewSet):
    queryset = Question.objects.all().order_by('-created_at')
    serializer_class = QuestionSerializer

    def get_queryset(self, **kwargs): # Override
        owner = self.kwargs['writer']
        return self.queryset.filter(writer=owner)
    
#제공하는 추천 질문
class RecQuestionViewSet(ModelViewSet):
    queryset = RecQuestion.objects.all()
    serializer_class = RecQuestionSerializer
    #authentication_classes = [BasicAuthentication, SessionAuthentication]

#제 3자가 보낸 질문(누구나 질문을 보낼 수 있음)
class BeQuestionViewSet(ModelViewSet):
    queryset = BeQuestion.objects.all()
    serializer_class = BeQuestionSerializer
    authentication_classes = [TokenAuthentication]
    #authentication_classes = [BasicAuthentication, SessionAuthentication]
    #permission_classes = [IsOwnerBeOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == "create":
            return BeQuestionSerializer
        if self.action == "list":
            return BeQuestionDetailSerializer
        if self.action == "retrieve":
            return BeQuestionDetailSerializer
        if self.action == "update": 
            return BeQuestionDetailSerializer
        
        return BeQuestionSerializer

    def partial_update(self, serializer):
        if self.request.user.id != None:        #로그인 했음.
            loginUser = self.request.user
            serializer.save(ownerId=self.request.user)
            update_serial=BeQuestionSerializer(loginUser, data=self.request.data, partial=True)
            update_serial.accept = True
            print(update_serial.accept)
            if update_serial.is_valid():
                update_serial.save()

#UserId별 선물 받은 질문 리스트(post하면 accept이 True로..)
class BeQuestionListSet(ModelViewSet):
    queryset = BeQuestion.objects.all().order_by('-created_at')
    serializer_class = BeQuestionDetailSerializer
    # authentication_classes = [BasicAuthentication, SessionAuthentication]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self, **kwargs): # Override
        ownerId = self.kwargs['ownerId']
        return self.queryset.filter(ownerId=ownerId)
    
#답변 CRUD. create는 CommentCreateSerializer, 나머지는 CommentSerializer
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    #permission_classes = [IsOwnerOrReadOnly]
    
    def get_serializer_class(self): 
        writer = self.request.user
        if self.action == 'list':
            return CommentSerializer
        if self.action == 'retrieve':
            return CommentSerializer
        if self.action == 'create':
            return CommentCreateSerializer
        if self.action == 'update':
            return CommentSerializer
        return CommentCreateSerializer

    #답변 생성하면 포인트 +50                       -> 내 질문에 내가 답변하는거 막아야하나?
    def perform_create(self, serializer):
        if self.request.user.id == None:            # 로그인 안해도 답변 남길 수 있음
            serializer.save(writer=self.request.user.id)
        else:                                       # 로그인 유저는 답변 남기면 포인트 +50
            loginUser = self.request.user
            serializer.save(writer=self.request.user)
            loginUser.point += 50
            update_serial=PointSerializer(loginUser, data=self.request.data, partial=True)
            if update_serial.is_valid():
                update_serial.save()

    #답변 누르면 포인트 차감
    def retrieve(self, request, pk=None, **kwargs):
        question_id = self.kwargs['questionId']
        question = get_object_or_404(Question, questionId=question_id)  # questionId로 해당 질문 받아옴
        # print(question.writer.id)                               # 질문 작성자 ID
        if self.request.user.id != None:                        # 로그인 했을때
            comment = Comment.objects.all()
            comment = get_object_or_404(Comment, commentId=pk)
            if comment.open_user.filter(id=request.user.id).exists():       # open_user로 flag처럼 사용해야 하는데..
                print('이미 열어본 답변')
                serializer=CommentSerializer(comment)
                print(serializer.data.keys)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                print('처음 열어보는 답변')
                comment.open_user.add(request.user)
                loginUser = request.user
                if loginUser.id == question.writer.id:          # 질문 작성자와 로그인 유저가 같음 -> 내 질문 내가 보는거
                    loginUser.point -= 50
                else:                                           # 질문 작성자와 로그인 유저가 다름 -> 남 질문 내가 보기
                    print('-100')   
                    loginUser.point -= 100
                update_serial=PointSerializer(loginUser, data=request.data, partial=True)

                if update_serial.is_valid():
                    update_serial.save()
                    serializer=CommentSerializer(comment)

                return Response(serializer.data, status=status.HTTP_200_OK)
        #로그인 안했을때 어떻게 해야할지?!?!
        else:                                                    # 로그인 안했을때
            print('로그인후 이용해주세요')
            serializer=LoginSerializer()
        return Response(serializer.data, status=status.HTTP_401_UNAUTHORIZED)
        
    #답변 공개 여부
    def update(self, request, *args,**kwargs):
        question_id = self.kwargs['questionId']
        question = get_object_or_404(Question, questionId=question_id)  # questionId로 해당 질문 받아옴
        comment_id = self.kwargs['pk']
        comment = get_object_or_404(Comment, pk=comment_id)

        if self.request.user.id != None:        #로그인 했음.
            loginUser = self.request.user
            print('답변 공개여부22')
            if question.writer.id == loginUser.id:
                print(question.writer.id)
                print(loginUser.id)
                update_serial=CommentSerializer(comment, data=self.request.data, partial=True)
                update_serial.publish = True
                if update_serial.is_valid():
                    update_serial.save()

                return Response(update_serial.data, status=status.HTTP_200_OK)
            
    def get_queryset(self, **kwargs): # Override
        question_id = self.kwargs['questionId']
        return self.queryset.filter(questionId=question_id)

#답변 추천
class CommentLikeViewSet(ModelViewSet):
    #authentication_classes = [BasicAuthentication, SessionAuthentication]          # 로그인 한 사람만 누를 수 있음
    authentication_classes = [TokenAuthentication]
    queryset = Comment.objects.all()    
    serializer_class = CommentLikeSerializer

    def get_serializer_class(self): 
        if self.action == 'list':
            return CommentLikeSerializer
        
    def list(self, request, **kwargs):
        comment_id = self.kwargs['pk']
        comment = get_object_or_404(Comment, pk=comment_id)
        serializer = CommentLikeSerializer(comment)

        access_token = self.request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        decoded = jwt.decode(access_token, algorithms=['HS256'], verify=False)
        user_id = decoded['user_id']
        loginUser = User.objects.get(pk=user_id)
        print(loginUser)
        
        if loginUser != None:                        # 로그인 했을때
            comment = get_object_or_404(Comment, pk=comment_id)
            if comment.like_user.filter(id=user_id).exists():          # 이미 추천 누른 경우
                print('이미 누름')
                comment.like_user.remove(loginUser)
                comment.like_count -= 1

            else:                                              # 추천 처음 누름
                if loginUser.id == comment.writer.id:          # 답변 작성자와 로그인 유저가 같음 -> 내 답변 내가 추천X
                    print('자기 답변 추천 금지')                
                else:                                          # 답변 작성자와 로그인 유저가 다름 -> 남 답변 내가 추천
                    print('남 답변 내가 추천')
                    comment.like_user.add(loginUser)
                    comment.like_count += 1
                    
            update_serial=CommentLikeSerializer(comment, data=request.data, partial=True)
            if update_serial.is_valid():
                update_serial.save()
                serializer=CommentLikeSerializer(comment)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def get_queryset(self, **kwargs): # Override
        comment_id = self.kwargs['comment_id']
        return self.queryset.filter(id=comment_id)
    
###########################################################################
class BeCommentViewSet(ModelViewSet):
    queryset = BeComment.objects.all().order_by('-created_at')
    #permission_classes = [IsOwnerOrReadOnly]
    
    def get_serializer_class(self): 
        if self.action == 'list':
            return BeCommentSerializer
        if self.action == 'retrieve':
            return BeCommentSerializer
        if self.action == 'create':
            return BeCommentCreateSerializer
        return BeCommentCreateSerializer

    #답변 생성하면 포인트 +50                       -> 내 질문에 내가 답변하는거 막아야하나?
    def perform_create(self, serializer):
        if self.request.user.id == None:            # 로그인 안해도 답변 남길 수 있음
            serializer.save(writer=self.request.user.id)
        else:                                       # 로그인 유저는 답변 남기면 포인트 +50
            access_token = self.request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            decoded = jwt.decode(access_token, algorithms=['HS256'], verify=False)
            user_id = decoded['user_id']
            writer = User.objects.get(pk=user_id)
            serializer.save(writer=writer)

            serializer.save(writer=writer)
            writer.point += 50
            update_serial=PointSerializer(writer, data=self.request.data, partial=True)
            if update_serial.is_valid():
                update_serial.save()

            # loginUser = self.request.user
            # serializer.save(writer=self.request.user)
            # loginUser.point += 50
            # update_serial=PointSerializer(loginUser, data=self.request.data, partial=True)
            # if update_serial.is_valid():
            #     update_serial.save()
        
    #답변 누르면 포인트 차감
    def retrieve(self, request, pk=None, **kwargs):
        question_id = self.kwargs['beQuestionId']
        question = get_object_or_404(BeQuestion, beQuestionId=question_id)  # questionId로 해당 질문 받아옴
        # print(question.writer.id)                               # 질문 작성자 ID
        if self.request.user.id != None:                        # 로그인 했을때
            comment = BeComment.objects.all()
            comment = get_object_or_404(BeComment, pk=pk)
            if comment.open_user.filter(id=request.user.id).exists():       # open_user로 flag처럼 사용해야 하는데..
                print('이미 열어본 답변')
                serializer=BeCommentSerializer(comment)
                print(serializer.data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                print('처음 열어보는 답변')
                comment.open_user.add(request.user)
                loginUser = request.user
                if loginUser.id == question.ownerId.id:          # 질문 작성자와 로그인 유저가 같음 -> 내 질문 내가 보는거
                    loginUser.point -= 50
                else:                                           # 질문 작성자와 로그인 유저가 다름 -> 남 질문 내가 보기
                    print('-100')   
                    loginUser.point -= 100
                update_serial=PointSerializer(loginUser, data=request.data, partial=True)

                if update_serial.is_valid():
                    update_serial.save()
                    serializer=BeCommentSerializer(comment)

                return Response(serializer.data, status=status.HTTP_200_OK)
        #로그인 안했을때 어떻게 해야할지?!?!
        else:                                                    # 로그인 안했을때
            print('로그인후 이용해주세요')
            serializer=LoginSerializer()
        return Response(serializer.data, status=status.HTTP_401_UNAUTHORIZED)
        
    def get_queryset(self, **kwargs): # Override
        question_id = self.kwargs['bequestion_id']
        print(question_id)
        return self.queryset.filter(questionId=question_id)

#답변 추천 로직
class BeCommentLikeViewSet(ModelViewSet):
    #authentication_classes = [BasicAuthentication, SessionAuthentication]          # 로그인 한 사람만 누를 수 있음
    authentication_classes = [TokenAuthentication]
    queryset = BeComment.objects.all()    
    serializer_class = BeCommentLikeSerializer

    def get_serializer_class(self): 
        if self.action == 'list':
            return BeCommentLikeSerializer
        
    def list(self, request, **kwargs):
        comment_id = self.kwargs['pk']
        comment = get_object_or_404(BeComment, pk=comment_id)
        serializer = BeCommentLikeSerializer(comment)

        access_token = self.request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        decoded = jwt.decode(access_token, algorithms=['HS256'], verify=False)
        user_id = decoded['user_id']
        loginUser = User.objects.get(pk=user_id)
        print(loginUser)
        
        if loginUser != None:                        # 로그인 했을때
            comment = get_object_or_404(BeComment, pk=comment_id)
            if comment.like_user.filter(id=user_id).exists():          # 이미 추천 누른 경우
                print('이미 누름')
                comment.like_user.remove(loginUser)
                comment.like_count -= 1

            else:                                              # 추천 처음 누름
                if loginUser.id == comment.writer.id:          # 답변 작성자와 로그인 유저가 같음 -> 내 답변 내가 추천X
                    print('자기 답변 추천 금지')                
                else:                                          # 답변 작성자와 로그인 유저가 다름 -> 남 답변 내가 추천
                    print('남 답변 내가 추천')
                    comment.like_user.add(loginUser)
                    comment.like_count += 1
                    
            update_serial=BeCommentLikeSerializer(comment, data=request.data, partial=True)
            if update_serial.is_valid():
                update_serial.save()
                serializer=BeCommentLikeSerializer(comment)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def get_queryset(self, **kwargs): # Override
        comment_id = self.kwargs['becomment_id']
        return self.queryset.filter(id=comment_id)