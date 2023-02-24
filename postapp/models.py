from django.db import models
from login.models import User
from django.conf import settings
from django.utils import timezone

class Question(models.Model):
    question = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question', null = True) #질문 작성자
    created_at = models.DateTimeField(auto_now_add=True, null=True)
 
    def __str__(self):
        return self.question


class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="comments")     #질문 ID
    comment = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null = True, blank=True)
    anonymous = models.BooleanField(default=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.comment

class OpenComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='openComments')
    reader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='openComments')
    is_seen = models.BooleanField(default=False)
