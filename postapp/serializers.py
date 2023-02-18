from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import Question, Comment
from login.models import User

class CommentSerializer(ModelSerializer):
    # comment_writer = ReadOnlyField(source='User.username')
    # user = serializers.ReadOnlyField(source = 'user.nickname')
    class Meta:
        model = Comment
        fields = ['id', 'comment', 'comment_writer', 'question']

class QuestionSerializer(ModelSerializer):
    # question_writer = ReadOnlyField(source='Profile.user.username')
    class Meta:
        model = Question
        fields = ['id', 'question', 'question_writer']

class QuestionDetailSerializer(ModelSerializer):
    # question_writer = ReadOnlyField(source='User.username')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question', 'question_writer', 'comments']