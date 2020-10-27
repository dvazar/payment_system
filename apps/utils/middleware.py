from rest_framework import status

from django.http import JsonResponse

from .exceptions import DomainException


class DomainExceptionMiddleware:
    """
    Returns error response on DomainException exception.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):  # NOQA
        if isinstance(exception, DomainException):
            data = {
                'code': 'invalid',
                'message': str(exception),
            }
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
