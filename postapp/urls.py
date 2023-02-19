from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import QuestionViewSet, CommentViewSet
from . import views


question_router = SimpleRouter(trailing_slash=False) 
question_router.register('questions', QuestionViewSet, basename='question')

comment_router = SimpleRouter(trailing_slash=False)
comment_router.register('comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(question_router.urls)),                #질문 post
    path('questions/<int:question_id>/', include(comment_router.urls)),  #질문 수정/삭제
    path('comments/<int:comment_id>/',include(comment_router.urls)),    #질문에 답변 작성
    #path('/<int:comment_id>/',include(comment_router.urls))
 ]