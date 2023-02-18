from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    question = models.TextField()
    question_writer = models.ForeignKey('login.User', on_delete=models.CASCADE, related_name='question', null = True) #질문 작성자
    # User로 불러와야함 onetoone or ForeignKey?
    def __str__(self):
        return self.question


class Comment(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    question = models.ForeignKey('postapp.Question', on_delete=models.CASCADE, blank = True, related_name="comments")     #질문 ID
    comment = models.TextField()
    comment_writer =  models.ForeignKey('login.User', on_delete=models.CASCADE, blank = True, null = True)     #답변 작성자
    # User로 불러와야함 onetoone or ForeignKey?
    def __str__(self):
        return self.comment

