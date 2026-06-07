from rest_framework.views import APIView
from apps.utils.api_response import api_response
from apps.accounts.models import User
from apps.accounts.api.v1.serializers import *
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions import IsCustomer, IsAdmin
from rest_framework.parsers import MultiPartParser, FormParser
@extend_schema(
    request=RegisterSerializer,
    responses={
        200: OpenApiResponse(description="User registered successfully"),
        400: OpenApiResponse(description="Registration failed"),
    },
    tags=["Accounts"],
)
class RegisterView(APIView):
    parser_classes = [MultiPartParser, FormParser]  # To handle file uploads
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print("User created:", user)
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
            if user.role in [User.Roles.CUSTOMER, User.Roles.ADMIN]:
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

@extend_schema(
    tags = ["Accounts"],
    summary="Customer Logout",
    description="Logout the authenticated user by blacklisting their refresh token.",
    request=LogoutSerializer,
    responses={
        200: {"description": "Logout Successful"},
        400: {"description": "Invalid or already blacklisted token"},
    },
)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Only logged-in users can logout

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            return api_response(
                success=True,
                message="Logout successfully!",
                data=None,
                errors=None,
                status_code=200
            )
        return api_response(
            success=False, 
            message="Logout failed!",
            data=None,
            errors=serializer.errors,
            status_code=400
        )
