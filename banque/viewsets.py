"""Banque app Actions viewset."""
import logging

from django.shortcuts import get_object_or_404

from tools.viewsets import ActionAPIView

from .models import Banque
from .serializers import BanqueSerializers

logger = logging.getLogger(__name__)


class BanqueViewSet(ActionAPIView):
    """Banque Actions viewsets."""

    def get_banque(self, request, params={}, *args, **kwargs):
        """Retrive banks."""
        serializer_context = {
            "request": request,
        }
        if "iso" in params:
            queryset = Banque.objects.filter(pays__id=params["iso"])
            serializer = BanqueSerializers(
                queryset, context=serializer_context, many=True
            )
            logger.debug("**retrieving country banks **")
            return {"success": True, "banque": serializer.data}
        """Get all bank."""
        get_all_bank = Banque.objects.all()
        serialized_banque = BanqueSerializers(get_all_bank, many=True).data
        return {"success": True, "banque": serialized_banque}

    get_banque.__doc__ = "Get all  banque"

    def create_banque(self, request, params={}, *args, **kwargs):
        """
         Create banque.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        serializer_context = {
            "request": request,
        }
        if isinstance(request.data.get("banque", None), list):
            banques = request.data.pop("banque")
            banque_objects = []
            for banque in banques:
                serializer = BanqueSerializers(data=banque, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                banque_objects.append(serializer)
            saved_banques = [model.save() for model in banque_objects]
            serialized_banques = BanqueSerializers(
                saved_banques, many=True, context=serializer_context
            )
            return {"success": True, "banque": serialized_banques.data}
        serializer = BanqueSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "banque": serializer.data}

    def update_banque(self, request, params={}, *args, **kwargs):
        """
         Update banque.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        serializer_context = {
            "request": request,
        }
        if isinstance(request.data.get("banque", None), list):
            banques = request.data.pop("banque")
            for banque in banques:
                instance = Banque.objects.get(pk=params.get("id", None))
                serializer = BanqueSerializers(
                    instance, data=banque, context=serializer_context
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return {"success": True, "banque": serializer.data}
        instance = get_object_or_404(Banque, pk=params.get("id", None))
        serializer = BanqueSerializers(
            instance, data=request.data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "banque": serializer.data}
