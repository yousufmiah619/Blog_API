from django.urls import path
from .views import RegisterAPIView,LoginAPIView,LogoutAPIView,UserProfileView,UpdateUserProfileView,ChangePasswordView


urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(),name='register'),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='logout'),
    path('user/profile', UserProfileView.as_view(), name='user-profile'),
    path('update/user/profile', UpdateUserProfileView.as_view(), name='update-user-profile'),
     path("user/change-password", ChangePasswordView.as_view(), name="change-password"),
]