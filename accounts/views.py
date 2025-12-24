from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens  import RefreshToken
from rest_framework.permissions import AllowAny
from .serializers import  RegisterSerializer,LoginSerializer,LogoutSerializer,UserProfileSerializer,UpdateUserProfileSerializer,ChangePasswordSerializer

class RegisterAPIView(APIView):
    def post(self,request):
        permission_classes = [AllowAny]
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
    permission_classes = [AllowAny]
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
        

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)

        return Response({
            "success": True,
            "message": "Profile retrieved successfully",
            "data": {
                "user": serializer.data
            }
        }, status=status.HTTP_200_OK)
        

class UpdateUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UpdateUserProfileSerializer(
            instance=request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Profile updated successfully",
                "data": None
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "message": "Validation error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            current_password = serializer.validated_data.get("current_password")
            new_password = serializer.validated_data.get("new_password")

            # current password check
            if not user.check_password(current_password):
                return Response({
                    "success": False,
                    "message": "Current password is incorrect",
                    "data": None
                }, status=status.HTTP_401_UNAUTHORIZED)

            # set new password
            user.set_password(new_password)
            user.save()

            return Response({
                "success": True,
                "message": "Password changed successfully",
                "data": None
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "message": "Validation error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)