from django.shortcuts import render

# Create your views here.
from .models import Question, Comment
from .serializers import QuestionSerializer, QuestionDetailSerializer, CommentSerializer
from rest_framework.viewsets import ModelViewSet


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return QuestionSerializer
        if self.action == "list":
            return QuestionDetailSerializer
        if self.action == "retrieve":
            return QuestionDetailSerializer
        
        return QuestionSerializer

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer   
    
    def get_queryset(self, **kwargs): # Override
        question_id = self.kwargs['pk']
        return self.queryset.filter(question=question_id)
