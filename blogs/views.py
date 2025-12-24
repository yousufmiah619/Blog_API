from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Post
from rest_framework.permissions import AllowAny
from django.core.paginator import Paginator
from .serializers import PostCreateUpdateSerializer,PostListSerializer


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
