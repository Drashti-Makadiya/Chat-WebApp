from rest_framework.response import Response

def api_response(success, message, status_code, data=None, errors=None):
    return Response({
        "success": success,
        "message": message,
        "data": data,
        "errors": errors,
        "status_code": status_code
    }, status=status_code)
    