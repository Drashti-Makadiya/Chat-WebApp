from rest_framework.views import APIView
from apps.utils.api_response import api_response
from apps.accounts.models import User
from apps.accounts.api.v1.serializers import *
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter

@extend_schema(
    request=RegisterSerializer,
    responses={
        200: OpenApiResponse(description="User registered successfully"),
        400: OpenApiResponse(description="Registration failed"),
    },
    tags=["Accounts"],
)
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return api_response(success=True, message="User registered successfully", data=None, status_code=201)
        return api_response(success=False, message="Registration failed", errors=serializer.errors, status_code=400)
    
@extend_schema(
    tags = ["Accounts"],
    summary="Customer Login",
    description="Login to customer account using email and password.",
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(response=LoginResponseSerializer),
        400: OpenApiResponse(description="Invalid email or password"),
        401: OpenApiResponse(description="Unauthorized access")
    },
)
class LoginView(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            
            user = serializer.validated_data["user"]
            if user.role in [User.Role.CUSTOMER, User.Role.ADMIN, User.Role.SUPER_ADMIN]:
                data = {
                    "access_token": serializer.validated_data["access"],
                    "refresh_token": serializer.validated_data["refresh"],
                    "user": {"id": user.pk, "email": user.email, "role": user.role},
                }
                return api_response(success=True, message="Login Successful!!", data=data, errors=None, status_code=200)
            else:
                return api_response(success=False, message="Unauthorized access.", data=None, errors=serializer.errors, status_code=401)

        except Exception as e:
            # Check if errors come from serializer validation
            errors = getattr(e, 'detail', str(e))
            return api_response(
                success=False,
                status_code=400, 
                message="Invalid email or password", 
                errors=serializer.errors
            )

