from django.db import models
from login.models import User
from django.conf import settings
from django.utils import timezone

class Question(models.Model):
    questionId = models.AutoField(primary_key=True)
    question = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question', null = True) #질문 작성자
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.question


#제공하는 질문들
class RecQuestion(models.Model):
    #질문 내용
    q = models.TextField()
    #질문 id 자동 생성
    #used??이거 뭐지
    used = models.IntegerField(default=0)

    def __str__(self):
        return self.q
    

#제 3자가 보낸 질문
class BeQuestion(models.Model):
    beQuestionId = models.AutoField(primary_key=True)
    q = models.TextField()
    ownerId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='beQuestion', null = True)
    accept = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.q
    

class Comment(models.Model):
    commentId = models.AutoField(primary_key=True)
    questionId = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="comments")     #질문 ID
    comment = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null = True, blank=True)
    anonymous = models.BooleanField(default=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    open_user = models.ManyToManyField(User, related_name='open_users')
    open_count = models.PositiveIntegerField(default=0, null=True)

    like_user = models.ManyToManyField(User, related_name='like_users')
    like_count = models.PositiveIntegerField(default=0, null=True)
    #답변 공개 여부
    publish = models.BooleanField(default=True, null=True)

    def __str__(self):
        return self.comment
    
class BeComment(models.Model):
    beCommentId = models.AutoField(primary_key=True)
    questionId = models.ForeignKey(BeQuestion, on_delete=models.CASCADE, related_name="beComments")     #질문 ID
    comment = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='beComments', null = True, blank=True)
    anonymous = models.BooleanField(default=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    open_user = models.ManyToManyField(User, related_name='beOpen_users')
    like_user = models.ManyToManyField(User, related_name='beLike_users')
    like_count = models.PositiveIntegerField(default=0, null=True)

    def __str__(self):
        return self.comment
