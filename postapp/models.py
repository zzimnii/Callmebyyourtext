from django.db import models
from django.contrib.auth.models import User, AnonymousUser

class Question(models.Model):
    question = models.TextField()
    writer = models.ForeignKey('login.User', on_delete=models.CASCADE, related_name='question', null = True) #질문 작성자
    # User로 불러와야함 onetoone or ForeignKey?
    def __str__(self):
        return self.question


class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="comments")     #질문 ID
    comment = models.TextField()
    writer = models.ForeignKey('login.User', on_delete=models.CASCADE, related_name='comments', null = True, blank=True)
    anonymous = models.BooleanField(default=True, blank=True, null=True)
    # comment_writer =  models.ForeignKey('login.User', on_delete=models.CASCADE, related_name='comments', default="익명", blank=True, null=True)     #답변 작성자
    # User로 불러와야함 onetoone or ForeignKey?
    def __str__(self):
        return self.comment