from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed({"error": "Invalid email or password"})

        if not user_obj.check_password(password):
            raise AuthenticationFailed({"error": "Invalid email or password"})

        if not user_obj.is_active:
            raise AuthenticationFailed({"error": "User account is disabled"})

        refresh = RefreshToken.for_user(user_obj)

        return {"token": str(refresh.access_token)}
