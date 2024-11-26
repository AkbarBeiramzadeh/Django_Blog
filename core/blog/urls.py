from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='post-list'),
    path('post/detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
]
