from django.urls import path, include
from .views import UserCreate, ProfileList, LoginView
 
urlpatterns = [
    path('signup/', UserCreate.as_view()),
    # path('signup/', include('rest_auth.registration.urls')),
    path('login/', LoginView.as_view()),
    path('profile/<int:pk>/', ProfileList.as_view()), # <int:pk> 써서 해당 계정 정보만 보여주게 해야함
                                             # => 권한이 있는지 확인 후 보여주기 or 안보여주기
    path('', include('rest_framework.urls')),
]