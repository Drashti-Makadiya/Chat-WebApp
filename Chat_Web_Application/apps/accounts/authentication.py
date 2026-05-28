from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from drf_spectacular.extensions import OpenApiAuthenticationExtension


class CustomJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):

        # SimpleJWT default authentication
        try:
            result = super().authenticate(request)
        except (InvalidToken, TokenError):
            raise AuthenticationFailed({
                "status": 401,
                "message": "Invalid or expired token"
            })
        if result is None:
            return None
        user, validated_token = result

        # Check if user active
        if not user.is_active:
            raise AuthenticationFailed({
                "status": 401,
                "message": "User account is inactive"
            })

        # Check blacklist
        jti = validated_token.get("jti")

        if BlacklistedToken.objects.filter(token__jti=jti).exists():
            raise AuthenticationFailed({
                "status": 401,
                "message": "Token has been blacklisted. Please login again."
            })
        return (user, validated_token)


# Swagger Authentication Support
class CustomJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "apps.accounts.authentication.CustomJWTAuthentication"
    name = "BearerAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
        