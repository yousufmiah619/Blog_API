from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Post,Category,Comment
from rest_framework.permissions import AllowAny
from django.core.paginator import Paginator
from .serializers import PostCreateUpdateSerializer,PostListSerializer,CategoryListSerializer,CategoryDetailSerializer,CommentSerializer

class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({
                "success": True,
                "message": "Post created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostCreateUpdateSerializer(post)
        return Response({
            "success": True,
            "message": "Post retrieved successfully",
            "data": serializer.data
        })


class PostUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk, author=request.user)
        serializer = PostCreateUpdateSerializer(post, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Post updated successfully",
                "data": serializer.data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk, author=request.user)
        post.delete()
        return Response({
            "success": True,
            "message": "Post deleted successfully",
            "data": None
        }, status=status.HTTP_200_OK)


class PostListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        page = int(request.GET.get("page", 1))
        per_page = min(int(request.GET.get("per_page", 10)), 20)

        queryset = (
            Post.objects
            .select_related("author")
            .prefetch_related("categories", "likes", "comments", "bookmarks")
            .order_by("-created_at")
        )

        paginator = Paginator(queryset, per_page)
        posts_page = paginator.get_page(page)

        serializer = PostListSerializer(
            posts_page,
            many=True,
            context={"request": request}
        )

        return Response({
            "success": True,
            "message": "Posts retrieved successfully",
            "data": {
                "posts": serializer.data,
                "pagination": {
                    "current_page": page,
                    "per_page": per_page,
                    "total_posts": paginator.count,
                    "total_pages": paginator.num_pages
                }
            }
        })

class CategoryListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = Category.objects.all().order_by('name')
        serializer = CategoryListSerializer(categories, many=True)

        return Response({
            "success": True,
            "message": "Categories retrieved successfully",
            "data": {
                "categories": serializer.data
            }
        })
class CategoryDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategoryDetailSerializer(category)

        return Response({
            "success": True,
            "message": "Category retrieved successfully",
            "data": {
                "category": serializer.data
            }
        })

class AddCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        post_id = request.data.get('post_id')
        content = request.data.get('content')
        parent_id = request.data.get('parent_id', 0)

        if not content:
            return Response(
                {"success": False, "message": "Content is required"},
                status=422
            )

        post = get_object_or_404(Post, id=post_id)

        parent = None
        if parent_id and int(parent_id) != 0:
            parent = get_object_or_404(Comment, id=parent_id)

        comment = Comment.objects.create(
            post=post,
            user=request.user,
            parent=parent,
            content=content
        )

        serializer = CommentSerializer(comment)

        return Response({
            "success": True,
            "message": "Comment added successfully",
            "data": {
                "comment": serializer.data
            }
        }, status=status.HTTP_201_CREATED)

class PostCommentListView(APIView):
    def get(self, request, post_id):
        page = int(request.GET.get('page', 1))
        per_page = min(int(request.GET.get('per_page', 20)), 50)

        comments = Comment.objects.filter(
            post_id=post_id,
            parent__isnull=True
        ).select_related('user').prefetch_related('replies')

        paginator = Paginator(comments, per_page)
        page_obj = paginator.get_page(page)

        serializer = CommentSerializer(page_obj, many=True)

        return Response({
            "success": True,
            "message": "Comments retrieved successfully",
            "data": {
                "comments": serializer.data,
                "pagination": {
                    "current_page": page,
                    "per_page": per_page,
                    "total_comments": paginator.count,
                    "total_pages": paginator.num_pages
                }
            }
        })

class UpdateCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)

        if comment.user != request.user:
            return Response(
                {"message": "Not comment owner"},
                status=status.HTTP_403_FORBIDDEN
            )

        comment.content = request.data.get('content', comment.content)
        comment.save()

        return Response({
            "success": True,
            "message": "Comment updated successfully",
            "data": {
                "comment": {
                    "id": comment.id,
                    "content": comment.content,
                    "updated_at": comment.updated_at
                }
            }
        })

class DeleteCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)

        if comment.user != request.user:
            return Response(
                {"message": "Not comment owner"},
                status=status.HTTP_403_FORBIDDEN
            )

        comment.delete()

        return Response({
            "success": True,
            "message": "Comment deleted successfully",
            "data": None
        })
