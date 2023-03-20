from django.urls import path, include
from .views import UserCreate, ProfileList, LoginView, LogoutView


urlpatterns = [
    path('signup/', UserCreate.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profile/<int:pk>/', ProfileList.as_view()), 

    path('', include('rest_framework.urls')),
]