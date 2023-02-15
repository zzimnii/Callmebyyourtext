# from django.urls import path, include
# from . import views
# from rest_framework.urlpatterns import format_suffix_patterns
# from rest_framework import urls

# urlpatterns = [
#     path('signup/', views.UserCreate.as_view(), name='login'),
#     path('signup/<int:pk>/', views.UserDetail.as_view(), name='edit'), # /pk 들어가면 회원 detail(수정, 삭제)
#     path('user/<int:pk>/', views.UserPage.as_view(), name='check'),  # 회원정보 조회
#     # path('api-auth/', include('rest_framework.urls')), # superuser로 로그인하면 404에러뜸 그래서 주석처리
# ]

# urlpatterns = format_suffix_patterns(urlpatterns)

from django.urls import path, include
from .api import RegisterAPI, LoginAPI, UserAPI
from knox import views as knox_views
 
urlpatterns = [
    path('api.auth', include('knox.urls')),
    path('api/auth/register', RegisterAPI.as_view()),
    path('api/auth/login', LoginAPI.as_view()),
    path('api/auth/user', UserAPI.as_view()),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
]

# from django.urls import path, include

# urlpatterns = [
#     path('rest-auth/', include('rest_auth.urls')),
#     path('rest-auth/registration/', include('rest_auth.registration.urls')),
# ]