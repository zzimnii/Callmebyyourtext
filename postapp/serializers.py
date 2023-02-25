from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ReadOnlyField
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .models import Question, Comment
from django.conf import settings
from datetime import datetime

class CommentSerializer(ModelSerializer):
    writer = serializers.ReadOnlyField(source = 'writer.name')
    class Meta:
        model = Comment
        fields = ['id','comment', 'questionId', 'writer', 'anonymous', 'created_at']


class CommentCreateSerializer(ModelSerializer):
    permission_classes = [AllowAny]
    class Meta:
        model = Comment
        fields = ['id', 'questionId', 'comment', 'anonymous', 'created_at']

    def create(self, validated_data):
        x = datetime.now()
        return Comment.objects.create(
            id = str(x.year)+str(x.month)+str(x.day)+str(x.hour)+str(x.minute)+str(x.second)+str(x.microsecond),
            comment=validated_data['comment'],
            writer=validated_data['writer'],
            anonymous=validated_data['anonymous'],
            questionId=validated_data['questionId']
            )


class QuestionSerializer(ModelSerializer):
    writer = serializers.ReadOnlyField(source = 'writer.name')
    class Meta:
        model = Question
        fields = ['id', 'question', 'writer', 'created_at']

    def create(self, validated_data):
        x = datetime.now()
        return Question.objects.create(
            id = str(x.year)+str(x.month)+str(x.day)+str(x.hour)+str(x.minute)+str(x.second)+str(x.microsecond),
            writer=validated_data['writer'],
            question=validated_data['question']
            )

class QuestionDetailSerializer(ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    writer = serializers.ReadOnlyField(source = 'writer.name')
    class Meta:
        model = Question
        fields = ['id', 'question', 'writer', 'comments', 'created_at']
