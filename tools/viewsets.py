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
    action = ''
    permission_classes = [permissions.IsAuthenticated]
    _last_action = None
    success = True
    RESPONSE_KEYS = ["user", "action", "token", "subject", "type", "messageid"]

    def get_permissions(self):
        # Instances and returns the dict of permissions that the view requires.
        if isinstance(self.permission_classes, list):
            return [permission() for permission in self.permission_classes]
        else:
             return {key: [permission() for permission in permissions] for key, permissions in
                self.permission_classes.items()}

    def check_permissions(self, request, action):
        # Gets the request method and the permissions dict,
        # and checks the permissions defined in the key matching
        # the method.
        method = request.method.lower()
        params = self.normalize_params(request)
        self._last_action = params.get("action", self.args)
        if isinstance(self.permission_classes, list):
            for permission in self.get_permissions():
                if not permission.has_permission(request, self):
                    self.permission_denied(
                        request,
                        message=getattr(permission, 'message', None),
                        code=getattr(permission, 'code', None)
                    )
        else:
            for permission in self.get_permissions()[action]:
                if not permission.has_permission(request, self):
                    self.permission_denied(
                        request, message=getattr(permission, 'message', None)
                    )

    def initial(self, request, *args, **kwargs):
        """
        Runs anything that needs to occur prior to calling the method handler.
        """
        self.format_kwarg = self.get_format_suffix(**kwargs)

        # Perform content negotiation and store the accepted info on the request
        neg = self.perform_content_negotiation(request)
        request.accepted_renderer, request.accepted_media_type = neg

        # Determine the API version, if versioning is in use.
        version, scheme = self.determine_version(request, *args, **kwargs)
        request.version, request.versioning_scheme = version, scheme

        # Ensure that the incoming request is permitted
        self.perform_authentication(request)
        self.check_permissions(request, kwargs.get('action', None))
        self.check_throttles(request)

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
            lv_action = self.action_does_not_exist
            response_status = 404
        # check permissions before
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
