from django.urls import path
from .views import (
    PostCreateView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    PostListView
)

urlpatterns = [
    path('posts/create/', PostCreateView.as_view()),
    path('posts/<int:pk>/', PostDetailView.as_view()),
    path('posts/<int:pk>/update/', PostUpdateView.as_view()),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view()),
    path("posts", PostListView.as_view()),
]
