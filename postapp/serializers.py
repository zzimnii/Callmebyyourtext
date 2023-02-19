from rest_framework.serializers import ModelSerializer, ReadOnlyField
from rest_framework.permissions import AllowAny
from .models import Question, Comment, AnonymousComment
from login.models import User

class AnonymousCommentSerializer(ModelSerializer):
    class Meta:
        model = AnonymousComment
        fields = []

class CommentSerializer(ModelSerializer):
    writer = ReadOnlyField(source = 'login.User')
    class Meta:
        model = Comment
        fields = ['id','comment', 'question', 'writer', 'anonymous']
        
class CommentCreateSerializer(ModelSerializer):
    permission_classes = [AllowAny]
    #comment_writer = ReadOnlyField(source = 'login.User')
    class Meta:
        model = Comment
        fields = ['id', 'question', 'comment', 'anonymous']


class QuestionSerializer(ModelSerializer):
    writer = ReadOnlyField(source = 'login.User')
    class Meta:
        model = Question
        fields = ['id', 'question', 'writer']

class QuestionDetailSerializer(ModelSerializer):
    writer = ReadOnlyField(source = 'login.User')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question', 'writer', 'comments']