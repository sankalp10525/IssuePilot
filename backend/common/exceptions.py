"""
Custom exception handler.
"""
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler as drf_exception_handler


class BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Bad request."
    default_code = "bad_request"


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Not found."
    default_code = "not_found"


class Forbidden(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "You do not have permission to perform this action."
    default_code = "forbidden"


def custom_exception_handler(exc, context):
    """Custom exception handler for DRF."""
    response = drf_exception_handler(exc, context)

    if response is not None:
        # Customize error response format
        response.data = {
            "error": {
                "message": response.data.get("detail", str(exc)),
                "code": getattr(exc, "default_code", "error"),
                "status_code": response.status_code,
            }
        }

    return response
