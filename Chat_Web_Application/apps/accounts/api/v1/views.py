from rest_framework.views import APIView
from apps.utils.api_response import api_response
from apps.accounts.models import User
from apps.accounts.api.v1.serializers import RegisterSerializer
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