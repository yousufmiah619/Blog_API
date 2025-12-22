from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens  import RefreshToken
from .serializers import  RegisterSerializer


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