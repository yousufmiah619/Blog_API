from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Blog
from .serializers import BlogSerializer

@api_view(['GET', 'POST'])
def blog_list_create(request):
    if request.method == 'GET':
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
