from django.urls import path, include
from .views import UserCreate, ProfileList
 
urlpatterns = [
    # path('register/', RegisterView.as_view()),
    # path('login/', LoginView.as_view()),
    # path('profile/<int:pk>/', ProfileView.as_view()),
    path('signup/', UserCreate.as_view()),
    path('', include('rest_framework.urls')),
    path('info/', ProfileList.as_view()),
]