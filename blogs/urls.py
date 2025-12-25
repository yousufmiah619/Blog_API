from django.urls import path
from .views import (
    PostCreateView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    PostListView,
    CategoryListView,
    CategoryDetailView, AddCommentView,
    PostCommentListView,
    UpdateCommentView,
    DeleteCommentView,
    LikePostView,
    UnlikePostView,
    PostLikesCountView,
    UserLikedPostsView
)

urlpatterns = [
    path('posts/create/', PostCreateView.as_view()),
    path('posts/<int:pk>/', PostDetailView.as_view()),
    path('posts/<int:pk>/update/', PostUpdateView.as_view()),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view()),
    path("posts", PostListView.as_view()),
    path('categories/', CategoryListView.as_view()),
    path('categories/<int:pk>/', CategoryDetailView.as_view()),
    path('comments', AddCommentView.as_view()),
    path('comments/post/<int:post_id>/', PostCommentListView.as_view()),
    path('comments/<int:pk>/', UpdateCommentView.as_view()),
    path('comments/<int:pk>/delete', DeleteCommentView.as_view()),
     path('posts/<int:post_id>/like/', LikePostView.as_view()),
    path('posts/<int:post_id>/like/delete/', UnlikePostView.as_view()),
    path('posts/<int:post_id>/likes/', PostLikesCountView.as_view()),
    path('user/likes/', UserLikedPostsView.as_view()),
]
