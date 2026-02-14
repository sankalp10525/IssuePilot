"""
Custom middleware.
"""
import logging
import time

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    """Middleware to log requests."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log request
        start_time = time.time()
        
        # Process request
        response = self.get_response(request)
        
        # Log response
        duration = time.time() - start_time
        logger.info(
            f"{request.method} {request.path} "
            f"[{response.status_code}] "
            f"{duration:.2f}s"
        )
        
        return response
