
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

