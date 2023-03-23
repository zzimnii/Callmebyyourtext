from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import QuestionViewSet, CommentViewSet, QuestionListSet, CommentLikeViewSet, RecQuestionViewSet, BeQuestionViewSet, BeQuestionListSet, BeCommentViewSet, BeCommentLikeViewSet
from . import views


question_router = SimpleRouter(trailing_slash=False) 
question_router.register('questions', QuestionViewSet, basename='question')

questionList_router = SimpleRouter(trailing_slash=False)
questionList_router.register('questionList', QuestionListSet, basename='list')

comment_router = SimpleRouter(trailing_slash=False)
comment_router.register('comments', CommentViewSet, basename='comment')

commentLike_router = SimpleRouter(trailing_slash=False)
commentLike_router.register('likes', CommentLikeViewSet, basename='likes')

beQuestion_router = SimpleRouter(trailing_slash=False)
beQuestion_router.register('bequestions', BeQuestionViewSet, basename='beQuestion')

beQuestionList_router = SimpleRouter(trailing_slash=False)
beQuestionList_router.register('bequestionList', BeQuestionListSet, basename='beqlist')

beComment_router = SimpleRouter(trailing_slash=False)
beComment_router.register('becomments', BeCommentViewSet, basename='becomment')

beCommentLike_router = SimpleRouter(trailing_slash=False)
beCommentLike_router.register('belikes', BeCommentLikeViewSet, basename='belikes')

urlpatterns = [
    path('', include(question_router.urls)),                #질문 post
    path('<int:writer>/', include(questionList_router.urls)),

    # path('recQuestion/', include(question_router.urls)),
    path('', include(beQuestion_router.urls)),
    path('<int:ownerId>/', include(beQuestionList_router.urls)),
    path('bequestions/<int:bequestion_id>/', include(beComment_router.urls)),
    path('becomments/<int:becomment_id>/',include(beCommentLike_router.urls)),

    path('questions/<int:question_id>/', include(comment_router.urls)),  #질문 수정/삭제
    path('comments/<int:comment_id>/',include(comment_router.urls)),    #질문에 답변 작성
    path('comments/<int:comment_id>/',include(commentLike_router.urls)),
 ]