from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler


def get_response(message="", result={}, status=False, status_code=200):
    error_object = {
        "message": message,
        "result": result,
        "status": status,
        "status_code": status_code,
    }
    payload = dict({'data': error_object})
    return dict({'payload': error_object})

def get_error_message(error_dict):
    field = next(iter(error_dict))
    response = error_dict[next(iter(error_dict))]
    if isinstance(response, dict):
        response = get_error_message(response)
    elif isinstance(response, list):
        response_message = response[0]
        if isinstance(response_message, dict):
            response = "{}: {}".format(field, get_error_message(response_message))
        else:
            response = "{}: {}".format(field, response[0])
    return response


def handle_exception(exc, context):

    error_response = exception_handler(exc, context)
    # if isinstance(exc, ValidationError):
    if error_response is not None:
        error = error_response.data

        if isinstance(error, list) and error:
            if isinstance(error[0], dict):
                error_response.data = get_response(
                    message=get_error_message(error),
                    status_code=error_response.status_code,
                )

            elif isinstance(error[0], str):
                error_response.data = get_response(
                    message=error[0], status_code=error_response.status_code
                )

        if isinstance(error, dict):
            error_response.data = get_response(
                message=get_error_message(error), status_code=error_response.status_code
            )
    payload = {}
    payload['message'] = error_response
    # payload
    return error_response


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        data = response.data
        response.data = {}
        # print("data: {}".format(data))
        errors = []
        for field, value in data.items():
            # print("field: {}".format(field))
            errors.append("{} : {}".format(field, " ".join(value)))

        response.data["errors"] = errors
        response.data["status"] = False

        response.data["exception"] = str(exc)

    return response


class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)
        if response.status_code == 500:
            response = get_response(
                message="Internal server error, please try again later",
                status_code=response.status_code,
            )
            return JsonResponse(response, status=response.get("status_code", 500))

        if response.status_code == 404 and "Page not found" in str(response.content):
            response = get_response(
                message="Page not found, invalid url", status_code=response.status_code
            )
            return JsonResponse(response, status=response.get("status_code", 404))
        return response
