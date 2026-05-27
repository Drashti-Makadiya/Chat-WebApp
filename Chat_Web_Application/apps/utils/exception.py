from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from apps.utils.api_response import api_response
from rest_framework.exceptions import Throttled


def custom_exception_handler(exc, context):
    response = exception_handler(exc,context) # This is Django Rest Framework’s internal function that:
                                                # Converts exceptions into proper HTTP responses
                                                # Decides status code
                                                # Formats validation errors
                                                # Handles Authentication errors
                                                # Handles Permission errors
                                                # Handles NotFound, etc.
    if response is not None:
        response.data = {
            "success": False,
            "status_code": response.status_code,
            "message": str(exc),
            "data": None,
            "errors": response.data,
        }
    return response
