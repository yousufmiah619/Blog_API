from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate,get_user_model

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



User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

        user = authenticate(
            username=user_obj.username,
            password=password
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data['user'] = user
        return data
    
    

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh_token']
        return attrs

    def save(self):
        try:
            RefreshToken(self.token).blacklist()
        except Exception:
            raise serializers.ValidationError("Invalid token")


    
    
    
    
