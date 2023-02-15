from rest_framework.serializers import ModelSerializer
from .models import Question, Comment


class CommentSerializer(ModelSerializer):
    #user = serializers.ReadOnlyField(source = 'user.nickname')
    class Meta:
        model = Comment
        fields = ['id', 'comment', 'comment_writer', 'question']

class QuestionSerializer(ModelSerializer):
    #user = serializers.ReadOnlyField(source = 'user.nickname')
    class Meta:
        model = Question
        fields = ['id', 'question', 'question_writer']

class QuestionDetailSerializer(ModelSerializer):
    #user = serializers.ReadOnlyField(source = 'user.nickname')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question', 'question_writer', 'comments']