from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)

    class Meta:
        model = User          # ✅ MUST
        fields = ['name', 'email', 'password', 'phone']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "The email has already been taken"
            )
        return value

    def create(self, validated_data):
        name = validated_data.pop('name')

        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone')
        )
        user.first_name = name
        user.save()
        return user

# from rest_framework import serializers
# from django.contrib.auth import get_user_model

# User=get_user_model()

# class RegisterSerializer(serializers.ModelSerializer):
#     name=serializers.CharField(write_only=True)
    
#     class Meta:
#         model = User
#         fields=['name','email','password','phone']
#         extra_kwargs={
#             'password':{'write_only' : True}
#         }
        
#     def validate_email (self,value):
#         if User.objects.filter(email=value).exists():
#             raise serializers.ValidationError(
#                 {
#                     'field':'email',
#                     'message':'The email has alrady been taken',
#                     'code':"VALIDATION_1004"
#                 }
#             )
#         return value
    
#     def create(self, validated_data):
#         name=validated_data.pop ('name'),
#         user=User.objects.create_user(
#             username=validated_data['email'],
#             email=validated_data['email'],
#             password=validated_data['password'],
#             phone=validated_data.get('phone')
#         )
#         user.first_name=name
#         user.save()
#         return user