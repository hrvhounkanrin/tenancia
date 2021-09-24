"""Contrat Actions viewsets."""
import datetime
import logging

from django.db.models import Q
from django.shortcuts import get_object_or_404
from quittance.models import Quittance
from quittance.serializers import  QuittanceSerializers
from customuser.permissions import IsLessor, IsTenant
from tools.viewsets import ActionAPIView

from .models import Accesoireloyer, Contrat, ContratAccessoiresloyer
from .serializers import (
    AccesoireloyerSerializers,
    AgreementSerializer,
    ContratAccessoiresloyerSerializers,
    ContratSerializers,
)

logger = logging.getLogger(__name__)


class AccessoireloyerAction(ActionAPIView):
    """ContratAccessoireloyer actions viewet."""

    def get_accessoire(self, request, params={}, *args, **kwargs):
        """Get acessoires loyer."""
        serializer_context = {
            "request": request,
        }
        queryset = Accesoireloyer.objects.all()
        serializer = AccesoireloyerSerializers(
            queryset, many=True, context=serializer_context
        )
        return {"success": True, "payload": serializer.data}

    def create_accessoire(self, request, params={}, *args, **kwargs):
        """Create accessoireloyer."""
        serializer_context = {
            "request": request,
        }
        if isinstance(request.data.get("accessoire", None), list):
            accesoires = request.data.pop("accessoire")
            acc___objects = []
            for acc in accesoires:
                serializer = AccesoireloyerSerializers(
                    data=acc, context=serializer_context
                )
                serializer.is_valid(raise_exception=True)
                acc___objects.append(serializer)
            saved_acc = [model.save() for model in acc___objects]
            serialized_acc = AccesoireloyerSerializers(
                saved_acc, context=serializer_context, many=True
            )
            return {"success": True, "payload": serialized_acc.data}
        serializer = AccesoireloyerSerializers(
            data=request.data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "payload": serializer.data}

    def update_accessoire(self, request, params={}, *args, **kwargs):
        """
        Update Accessoire.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        serializer_context = {
            "request": request,
        }
        if isinstance(request.data.get("accessoire", None), list):
            accessoires = request.data.pop("accessoire")
            acc_objects = []
            for acc in accessoires:
                instance = Accesoireloyer.objects.get(pk=params.get("id", None))
                serializer = AccesoireloyerSerializers(
                    instance, data=acc, context=serializer_context
                )
                serializer.is_valid(raise_exception=True)
                acc_objects.append(serializer)
            saved_components = [model.save() for model in acc_objects]
            serializer = AccesoireloyerSerializers(
                saved_components, many=True, context=serializer_context
            )
            return {"success": True, "accessoireloyer": serializer.data}
        instance = get_object_or_404(Accesoireloyer, pk=params.get("id", None))
        serializer = AccesoireloyerSerializers(
            instance, data=request.data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "accessoire": serializer.data}


class ContratAccessoiresloyerAction(ActionAPIView):
    """ContratAccessoireloyer Action Viewset."""

    queryset = ContratAccessoiresloyer.objects.all()
    serializer_class = ContratAccessoiresloyerSerializers


class ContratAction(ActionAPIView):
    """Contrat Action viewset."""

    def __init__(self):
        self.permission_classes = {
            "get_lessor_contrat": [IsLessor],
            "get_tenant_contrat": [IsTenant],
            "create_contrat": [IsLessor],
            "update_contrat": [IsLessor],
            "contrat_agreement": [IsTenant],
        }

    def __filter_q_object(self, params):
        q_objects = Q()
        if "id" in params:
            q_objects &= Q(id=params["id"])
        if "immeuble_id" in params:
            q_objects &= Q(appartement__immeuble__id=params["immeuble_id"])
        if "appartement_id" in params:
            q_objects &= Q(appartement__id=params["appartement_id"])
        if "tenant" in params:
            q_objects &= (Q(client__user__last_name__istartswith=params["tenant"]) |
                          Q(client__user__first_name__istartswith=params["tenant"]))
        if "lessor" in params:
            q_objects &= (Q(appartement__immeuble__proprietaire__user__last_name__istartswith=params["lessor"]) |
                          Q(appartement__immeuble__proprietaire__user__first_name__istartswith=params["lessor"]))
        if "statut" in params:
            q_objects &= Q(statut__iexact=params["statut"])
        if "date_effet" in params and len(params["date_effet"]) == 1:
            q_objects &= Q(date_effet=params["date_effet"][0])
        if "date_effet" in params and len(params["date_effet"]) > 1:
            q_objects &= (Q(date_effet__gte=params["date_effet"][0]) &
                          Q(date_effet__lte=params["date_effet"][1]))
        if "prochaine_echeance" in params and len(params["prochaine_echeance"]) == 1:
            q_objects &= Q(date_effet=params["prochaine_echeance"][0])
        if "prochaine_echeance" in params and len(params["prochaine_echeance"]) > 1:
            q_objects &= (Q(date_effet__gte=params["prochaine_echeance"][0]) &
                          Q(date_effet__lte=params["prochaine_echeance"][1]))

        if "montant_bail" in params and len(params["montant_bail"]) == 1:
            q_objects &= Q(montant_bail=params["montant_bail"][0])
        if "montant_bail" in params and len(params["montant_bail"]) > 1:
            q_objects &= (Q(montant_bail__gte=params["montant_bail"][0]) &
                          Q(montant_bail__lte=params["montant_bail"][1]))
        return q_objects

    def get_lessor_contrat(self, request, params={}, *args, **kwargs):
        """Get contract portfolios for lessor or real_estate."""
        q_objects = self.__filter_q_object(params)
        q_objects &= (Q(created_by=request.user) | Q(appartement__immeuble__proprietaire__user=request.user))
        queryset = Contrat.objects.filter(q_objects)
        serializer = ContratSerializers(
            queryset, many=True, context={"request": request}
        )
        return {"success": True, "payload": serializer.data}

    def get_tenant_contrat(self, request, params={}, *args, **kwargs):
        """Get contrat."""
        if "id" in params:
            queryset = Contrat.objects.filter(id__in=params["id"].split(",")).filter(
                client__user=request.user
            )
            serializer = ContratSerializers(
                queryset, context={"request": request}, many=True
            )
            logger.debug("**retrieving Contrat **")
            return {"success": True, "payload": serializer.data}
        queryset = Contrat.objects.filter(
            client__user=request.user
        )
        serializer = ContratSerializers(
            queryset, many=True, context={"request": request}
        )
        return {"success": True, "payload": serializer.data}

    def create_contrat(self, request, params={}, *args, **kwargs):
        """Create contract."""
        serializer_context = {
            "request": request,
        }
        if isinstance(request.data.get("contrat", None), list):
            contrats = request.data.pop("contrat")
            contrat_objects = []
            for contrat in contrats:
                serializer = ContratSerializers(
                    data=contrat, context=serializer_context
                )
                serializer.is_valid(raise_exception=True)
                contrat_objects.append(serializer)
            saved_contrat = [model.save() for model in contrat_objects]
            serialized_contrat = ContratSerializers(
                saved_contrat, context=serializer_context, many=True
            )
            return {"success": True, "payload": serialized_contrat.data}
        serializer = ContratSerializers(data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "payload": serializer.data}

    def update_contrat(self, request, params={}, *args, **kwargs):
        """Update contract."""
        serializer_context = {
            "request": request,
        }
        if isinstance(request.data.get("contrat", None), list):
            contrats = request.data.pop("contrat")
            contrat_objects = []
            for contrat in contrats:
                serializer = ContratSerializers(
                    data=contrat, context=serializer_context
                )
                serializer.is_valid(raise_exception=True)
                contrat_objects.append(serializer)
            saved_contrat = [model.save() for model in contrat_objects]
            serialized_contrat = ContratSerializers(
                saved_contrat, context=serializer_context, many=True
            )
            return {"success": True, "contrat": serialized_contrat.data}
        serializer = ContratSerializers(data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "contrat": serializer.data}

    def contrat_agreement(self, request, params={}, **kwargs):
        serializer_context = {
            "request": request,
        }
        try:
            instance = Contrat.objects.get(pk=params.get("id", None))
        except:
            return {"success": False, "payload": dict({"message": "Ce contrat n'existe pas"}), "status_code": 400}

        serializer = AgreementSerializer(
            instance, data=params, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if params.get("client_accord", None) in [False, None]:
            return {"success": True, "payload": serializer.data}

        queryset = Quittance.objects.all()
        quittances_serializer = QuittanceSerializers(
            queryset, many=True, context={"request": request}
        )
        payload = serializer.data
        payload['quittances'] = quittances_serializer.data
        return {"success": True, "payload": payload}
