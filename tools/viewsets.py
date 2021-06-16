"""Misc viewset."""
import inspect
import logging

from django.http import HttpResponse, QueryDict
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .mes_api_serializers import APISerializer

logger = logging.getLogger("meslimmo")


class ActionAPIView(APIView):
    """
    Base class for action services taken by the new front end.

    The action function will be determined, if it exists and called.
    Each action function takes the request, expecting JSON body
    (if required) and returns a dictionary
    or Response instance.
    """

    permission_classes = [permissions.IsAuthenticated]
    _last_action = None
    success = True
    RESPONSE_KEYS = ["user", "action", "token", "subject", "type", "messageid"]

    def post(self, request, action, **kwargs):
        return self.get(request, action, **kwargs)

    def get(self, request, action, **kwargs):
        """I really don't what this func ain to."""
        params = self.normalize_params(request)
        kwargs["params"] = params
        self._last_action = params.get("action", action)
        response_status = 200
        try:
            lv_action = self.__getattribute__(self._last_action)
            # print(callable(getattr(self, 'exchange_token', None)))
            # print('self._last_action: {}'.format(type(self.__getattribute__(self._last_action))))
            # print('self._last_action decorator: {}'.format(get_decorators(lv_action)))
        except AttributeError:
            print("AttributeError tout de meme")
            lv_action = self.action_does_not_exist
            response_status = 404
        response = lv_action(request, **kwargs)
        if isinstance(response, (Response,)):
            response = response.data
        if isinstance(response, (HttpResponse,)):
            return response

        response_context = dict(
            filter(
                lambda item: item[1] is not None,
                {k: params.get(k, None) for k in self.RESPONSE_KEYS}.items(),
            )
        )
        serialised = APISerializer(response, context=response_context)
        return Response(serialised.data, response_status)

    def action_does_not_exist(self, *args, **kwargs):
        """I really don't what this func ain to."""
        return {
            "success": False,
            "reason": "Action '%s' does not exist." % self._last_action,
        }

    def normalize_params(self, request):
        """
        Combine the possible parameter sources from the request.

        :param request: a REST API request object
        :return: a combined dict of the 2 possible
        data sources from the request.
        """
        params = request.query_params.dict().copy()
        if isinstance(request.data, QueryDict):
            params.update(request.data.dict())
        else:
            params.update(request.data)
        return params


def is_exception(obj):
    """Return whether obj is an exception."""
    try:
        return issubclass(obj, BaseException)
    except TypeError:
        return isinstance(obj, BaseException)


def is_exception_class(obj):
    """Return whether obj is an exception class, or a tuple of the same."""
    try:
        if isinstance(obj, tuple):
            return obj and all(issubclass(X, BaseException) for X in obj)
        return issubclass(obj, BaseException)
    except TypeError:
        return False


def get_decorators(function):
    # If we have no func_closure, it means we are not wrapping any other functions.
    if not function.func_closure:
        return [function]
    decorators = []
    # Otherwise, we want to collect all of the recursive results for every closure we have.
    for closure in function.func_closure:
        decorators.extend(get_decorators(closure.cell_contents))
    return [function] + decorators
