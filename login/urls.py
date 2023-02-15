from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import urls

urlpatterns = [
    path('signup/', views.UserCreate.as_view(), name='login'),
    path('signup/<int:pk>/', views.UserDetail.as_view(), name='edit'), # /pk 들어가면 회원 detail(수정, 삭제)
    path('user/<int:pk>/', views.UserPage.as_view(), name='check'),  # 회원정보 조회
    # path('api-auth/', include('rest_framework.urls')), # superuser로 로그인하면 404에러뜸 그래서 주석처리
]

urlpatterns = format_suffix_patterns(urlpatterns)