from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ReadOnlyField
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .models import Question, Comment, RecQuestion, BeQuestion, BeComment
from login.models import User
from django.conf import settings
from datetime import datetime

class CommentSerializer(ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model=User
            fields=['id', 'name', 'point']

    open_user = UserSerializer(read_only=True, many=True)
    writer = serializers.ReadOnlyField(source = 'writer.name')
    class Meta:
        model = Comment
        fields = ['commentId','comment', 'questionId', 'writer', 'anonymous', 'created_at', 'open_user']

class CommentCreateSerializer(ModelSerializer):
    permission_classes = [AllowAny]
    class Meta:
        model = Comment
        fields = ['commentId', 'questionId', 'comment', 'anonymous', 'created_at']

    def create(self, validated_data):
        x = datetime.now()
        return Comment.objects.create(
            comment=validated_data['comment'],
            writer=validated_data['writer'],
            anonymous=validated_data['anonymous'],
            questionId=validated_data['questionId']
            )

class CommentLikeSerializer(ModelSerializer):
    def update(self, instance, validated_data):
        print(instance)
        instance.like_count = validated_data.get('like_count', instance.like_count)
        instance.save()
        return instance
    
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model=User
            fields=['id', 'name']
    
    like_user = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Comment
        fields=['commentId', 'like_user', 'like_count']  

###################################################     BeComment
class BeCommentSerializer(ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model=User
            fields=['id', 'name', 'point']

    open_user = UserSerializer(read_only=True, many=True)
    writer = serializers.ReadOnlyField(source = 'writer.name')
    class Meta:
        model = BeComment
        fields = ['beCommentId','comment', 'questionId', 'writer', 'anonymous', 'created_at', 'open_user']


class BeCommentCreateSerializer(ModelSerializer):
    permission_classes = [AllowAny]
    class Meta:
        model = BeComment
        fields = ['beCommentId', 'questionId', 'comment', 'anonymous', 'created_at']

    def create(self, validated_data):
        x = datetime.now()
        return BeComment.objects.create(
            comment=validated_data['comment'],
            writer=validated_data['writer'],
            anonymous=validated_data['anonymous'],
            questionId=validated_data['questionId']
            )

class BeCommentLikeSerializer(ModelSerializer):
    def update(self, instance, validated_data):
        print(instance)
        instance.like_count = validated_data.get('like_count', instance.like_count)
        instance.save()
        return instance
    
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model=User
            fields=['id', 'name']
    
    like_user = UserSerializer(read_only=True, many=True)

    class Meta:
        model = BeComment
        fields=['beCommentId', 'like_user', 'like_count']  
################################################################################################
class QuestionSerializer(ModelSerializer):
    writer = serializers.ReadOnlyField(source = 'writer.name')
    class Meta:
        model = Question
        fields = ['questionId', 'question', 'writer', 'created_at']

    def create(self, validated_data):
        x = datetime.now()
        return Question.objects.create(
            writer=validated_data['writer'],
            question=validated_data['question']
            )
        
class QuestionDetailSerializer(ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    writer = serializers.ReadOnlyField(source = 'writer.name')
    class Meta:
        model = Question
        fields = ['questionId', 'question', 'writer', 'comments', 'created_at']

class RecQuestionSerializer(ModelSerializer):
    class Meta:
        model = RecQuestion
        fields = ['id', 'q','used']

class BeQuestionSerializer(ModelSerializer):
    class Meta:
        model = BeQuestion
        fields = ['beQuestionId', 'q', 'ownerId', 'created_at']

    def create(self, validated_data):
        x = datetime.now()
        return BeQuestion.objects.create(
            q=validated_data['q'],
            ownerId=validated_data['ownerId']
            )
    
class BeQuestionDetailSerializer(ModelSerializer):
    beComments = BeCommentSerializer(many=True, read_only=True)
    class Meta:
        model = BeQuestion
        fields = ['beQuestionId', 'q', 'ownerId', 'beComments', 'created_at', 'accept']