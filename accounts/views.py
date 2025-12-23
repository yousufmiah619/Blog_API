from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens  import RefreshToken
from .serializers import  RegisterSerializer,LoginSerializer,LogoutSerializer


class RegisterAPIView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                "success": True,
                "message": "Registration successful",
                "data": {
                    "user": {
                        "id": user.id,
                        "name": user.first_name,
                        "email": user.email,
                        "phone": user.phone
                    },
                    "token": str(refresh.access_token),
                    "token_type": "Bearer",
                    "expires_in": 86400
                }
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "message": "Validation failed",
            "data": None,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            refresh = RefreshToken.for_user(user)

            return Response({
                "success": True,
                "message": "Login successful",
                "data": {
                    "user": {
                        "id": user.id,
                        "name": user.first_name,
                        "email": user.email,
                        "phone": user.phone
                    },
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "token_type": "Bearer",
                    "expires_in": 86400
                }
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "message": "Invalid credentials",
            "data": None
        }, status=status.HTTP_401_UNAUTHORIZED)
        
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Logged out successfully",
                "data": None
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "message": "Logout failed",
            "data": None
        }, status=status.HTTP_400_BAD_REQUEST)
        
 