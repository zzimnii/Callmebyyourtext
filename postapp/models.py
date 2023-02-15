from django.db import models


class Question(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    question = models.TextField()
    question_writer = models.ForeignKey('login.User', on_delete=models.CASCADE, related_name='question') #질문 작성자

    def __str__(self):
        return self.question


class Comment(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    question = models.ForeignKey('postapp.Question', on_delete=models.CASCADE, blank = True, related_name="comments")     #질문 ID
    comment = models.TextField()
    comment_writer =  models.ForeignKey('login.User', on_delete=models.CASCADE, blank = True)     #답변 작성자

    def __str__(self):
        return self.comment

