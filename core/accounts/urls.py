from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name="user_profile"),
    path('user/edit/', views.EditProfileView.as_view(), name="user_edit"),
    path('user/logout/', views.LogoutUserView.as_view(), name="user_logout"),

    path('api/v1/', include('accounts.api.v1.urls')),
]
