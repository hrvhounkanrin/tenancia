
from functools import wraps
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response
from django.http import HttpResponse, QueryDict
from rest_framework import viewsets, mixins, exceptions
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import permissions

# from application.models import State
# from tools.security import validate_parameters
from . mes_api_serializers import GenericModelSerializer, APISerializer
from rest_framework.parsers import JSONParser
# from rest_framework.renderers import JSONRenderer
# from tools.renderers import XMLRenderer
# from rest_framework.renderers import JSONRenderer
# from rest_framework_xml.parsers import XMLParser
# from rest_framework_xml.renderers import XMLRenderer
from rest_framework.parsers import FormParser, MultiPartParser
import uuid
# from tools.sanitize import *
import logging

logger = logging.getLogger('meslimmo')




class ActionAPIView(APIView):
    """
    Base class for action services taken by the new front end.
    The action function will be determined, if it exists and called.
    Each action function takes the request, expecting JSON body (if required) and returns a dictionary
    or Response instance
    """
    permission_classes = [permissions.IsAuthenticated]
    _last_action = None
    success = True
    RESPONSE_KEYS = ['user', 'action', 'token', 'subject', 'type', 'messageid']


    def post(self, request, action, **kwargs):
        return self.get(request, action, **kwargs)

    def get(self, request, action, **kwargs):
        params = self.normalize_params(request)
        kwargs['params'] = params
        self._last_action = params.get('action', action)
        try:
            lv_action = self.__getattribute__(self._last_action)
        except AttributeError:
            lv_action = self.action_does_not_exist
        response = lv_action(request, **kwargs)
        if isinstance(response, (Response, )):
            response = response.data
        if isinstance(response, (HttpResponse, )):
            return response

        response_context = dict(
            filter(lambda item: item[1] is not None, {
                k: params.get(k, None) for k in self.RESPONSE_KEYS
            }.items()))
        serialised = APISerializer(response, context=response_context)
        return Response(serialised.data)

    def action_does_not_exist(self, *args, **kwargs):
        return {'success': False, 'reason': "Action '%s' does not exist." % self._last_action}

    def normalize_params(self, request):
        """
        Combines the possible parameter sources from the request.
        :param request: a REST API request object
        :return: a combined dict of the 2 possible data sources from the request
        """
        params = request.query_params.dict().copy()
        if isinstance(request.data, QueryDict):
            params.update(request.data.dict())
        else:
            params.update(request.data)
        return params


class accom_socite_proprietaire_square(object):
    #TODO : Creating an  auto allocation Engine  has to be more explored
    #TODO : Ce que je veux dire .... est trop profond pour que j'explore :'((


    def __init(self,inner_man, societe,__check_proprietaire_, _aux_sur_contract):
        self.inner_man = inner_man
        self.societe = societe
        self.__check_proprietaire  = __check_proprietaire_
        self._aux_sur_contract = _aux_sur_contract



    def get_area_by_autolocate_client_to_proprio(self,x ,y):
        "Assumming We shoudl let the client who want to view the house which needs to be exposses should be based "
        return abs(sum(i * j for i, j in zip(x, y[1:])) + x[-1] * y[0]
                   - sum(i * j for i, j in zip(x[1:], y)) - x[0] * y[-1]) / 2


class exception_guard(object):
    """Guard against the given exception and raise a different exception.
       Will need to have a deep look to how the ActionAPiView will manage the exception
    """

    def __init__(self, catchable, throwable=RuntimeError):
        if is_exception_class(catchable):
            self._catchable = catchable
        else:
            raise TypeError('catchable must be one or more exception types')
        if throwable is None or is_exception(throwable):
            self._throwable = throwable
        else:
            raise TypeError('throwable must be None or an exception')

    def throw(self, cause):
        """Throw an exception from the given cause."""
        throwable = self._throwable
        assert throwable is not None
        self._raisefrom(throwable, cause)

    def _raisefrom(self, exception, cause):
        #TODO  : Function will expanded  in some few weeks have not sat down to think about the full exploration
        # "raise ... from ..." syntax only supported in Python 3.  Need to show that to Herve
        assert cause is not None  # "raise ... from None" is not supported.
        if isinstance(exception, BaseException):
            # We're given an exception instance, so just use it as-is.
            pass
        else:
            # We're given an exception class, so instantiate it with a
            # helpful error message.
            assert issubclass(exception, BaseException)
            name = type(cause).__name__
            message = 'guard triggered by %s exception' % name
            exception = exception(message)
        try:
            exec("raise exception from cause", globals(), locals())
        except SyntaxError:
            # Python too old. Fall back to a simple raise, without cause.
            raise exception

    # === Context manager special methods ===
    # ===So when Tenancia , will be running properly this fuction will be expanded

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None and issubclass(exc_type, self._catchable):
            if self._throwable is None:
                # Suppress the exception.
                return True
            else:
                self.throw(exc_value)

    # === Use exception_guard as a decorator ===

    def __call__(self, function):
        """
          This is a callable methoid to suppress the  exception when its thrown
        :param function:
        :return:
        """
        catchable = self._catchable
        suppress_exception = (self._throwable is None)
        @wraps(function)
        def inner(*args, **kwargs):
            try:
                result = function(*args, **kwargs)
            except catchable as error:
                if suppress_exception:
                    return
                else:
                    self.throw(error)
            else:
                return result
        return inner


# Two helper functions.

def is_exception(obj):
    """Return whether obj is an exception.
    False

    """
    try:
        return issubclass(obj, BaseException)
    except TypeError:
        return isinstance(obj, BaseException)

def is_exception_class(obj):
    """Return whether obj is an exception class, or a tuple of the same.
    True

    """
    try:
        if isinstance(obj, tuple):
            return obj and all(issubclass(X, BaseException) for X in obj)
        return issubclass(obj, BaseException)
    except TypeError:
        return False
