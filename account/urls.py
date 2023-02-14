from django.urls import path, include
from . import views
from rest_framework import urls

urlpatterns = [
    path('signup/', views.UserCreate.as_view()),
    # path('api-auth/', include('rest_framework.urls')), # superuser로 로그인하면 404에러뜸 그래서 주석처리
]