from rest_framework.views import APIView
from apps.utils.api_response import api_response
from apps.accounts.models import User
from apps.accounts.api.v1.serializers import RegisterSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return api_response(success=True, message="User registered successfully", data={"user_id": user.id})
        return api_response(success=False, message="Registration failed", errors=serializer.errors)