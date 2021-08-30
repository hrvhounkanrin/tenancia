"""Housing app Action viewset."""
import logging
from django.db.models import Max
from django.shortcuts import get_object_or_404

from appartement.models import Appartement, StructureAppartement, TypeDependence
from appartement.appartement_immebeule_serializer import AppartementImmeubleSerializers
from appartement.serializers import (
    AppartementSerializers,
    ClonerAppartementSerializer,
    StructureAppartmentSerializers,
    TypeDependenceSerializers,
)
from tools.viewsets import ActionAPIView
from customuser.permissions import IsLessor, IsTenant
logger = logging.getLogger(__name__)


class AppartementViewSet(ActionAPIView):
    """Housing Viewset."""

    def __init__(self):
        self.permission_classes = {
            "get_logement": [IsLessor],
            "create_logement": [IsLessor],
            "update_logement": [IsLessor],
            "cloner_immeuble": [IsLessor],
            "cloner_logement": [IsLessor],
        }


    def get_logement(self, request, params={}, *args, **kwargs):
        """Get housing."""
        serializer_context = {
            "request": request,
        }

        queryset = Appartement.objects.filter(created_by=self.request.user)
        if "id" in params:
            queryset = Appartement.objects.filter(
                id__in=params["id"].split(","), created_by=self.request.user
            )
        if "immeuble_id" in params:
            queryset = Appartement.objects.filter(
                immeuble_id=params["immeuble_id"], created_by=self.request.user
            )
        if "statut_appartement" in params and "query" in params:
            queryset = Appartement.objects.filter(created_by=self.request.user,
                                                  statut=params['statut_appartement'],
                                                  intitule__istartswith=params['query'])
            print("searching appartment: {}".format(params['statut_appartement']))
            serializer = AppartementImmeubleSerializers(
                queryset, context=serializer_context, many=True
            )
            logger.debug("**retrieving housing **")
            return {"success": True, "payload": serializer.data}

        serializer = AppartementSerializers(
            queryset, context=serializer_context, many=True
        )
        logger.debug("**retrieving housing **")
        return {"success": True, "payload": serializer.data}

    def create_logement(self, request, params={}, *args, **kwargs):
        """
         Create appartement.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        serializer_context = {
            "request": request,
        }
        if isinstance(request.data, list):
            appartements = request.data
            appart_objects = []
            for appart in appartements:
                serializer = AppartementSerializers(
                    data=appart, context=serializer_context
                )
                serializer.is_valid(raise_exception=True)
                appart_objects.append(serializer)
            saved_appartements = [
                model.save(created_by=request.user) for model in appart_objects
            ]
            serialized_proprio = AppartementSerializers(
                saved_appartements, many=True, context=serializer_context
            )
            return {"success": True, "payload": serialized_proprio.data}
        data = request.data
        if data['level'] is None or data['level'] == '':
            data['level'] = 0
        if data['intitule'] is None or data['intitule'] == '':
            data['intitule'] = self.__autoname(data['immeuble_id'], data['level'])
        serializer = AppartementSerializers(
            data=request.data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return {"success": True, "payload": serializer.data}

    def update_logement(self, request, params={}, *args, **kwargs):
        """
         Update appartement.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        serializer_context = {
            "request": request,
        }
        if isinstance(request.data.get("appartement", None), list):
            appartements = request.data.pop("appartement")
            for appart in appartements:
                instance = Appartement.objects.get(pk=params.get("id", None))
                serializer = AppartementSerializers(
                    instance, data=appart, context=serializer_context
                )
                serializer.is_valid(raise_exception=True)
                serializer.save(modified_by=request.user)
                return {"success": True, "payload": serializer.data}
        instance = get_object_or_404(Appartement, pk=params.get("id", None))
        serializer = AppartementSerializers(
            instance, data=request.data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(modified_by=request.user)
        return {"success": True, "payload": serializer.data}

    def cloner_logement(self, request, params={}, *args, **kwargs):
        """Multiplier un logement suivant un nombre et un id appartement"""
        """
                Create appartement.

               :param request:
               :param params:
               :param args:
               :param kwargs:
               :return:
               """
        serializer_context = {
            "request": request,
        }

        serializer = ClonerAppartementSerializer(
            data=request.data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return {"success": True, "payload": serializer.data}

    def __autoname(self, immeuble_id, level):
        last_intitule = Appartement.objects.filter(immeuble__id=immeuble_id, level=level)
        last_intitule = last_intitule.aggregate(Max('intitule'))['intitule__max']
        if last_intitule is None:
            return str(level) + '-A'
        return last_intitule[0:len(last_intitule) - 1] + chr(ord(last_intitule[-1]) + 1)

class ComposantAppartementViewSet(ActionAPIView):
    """Housing dependency Action Viewset."""

    def get_dependancies(self, request, params={}, *args, **kwargs):
        """Get all housing dependencies."""
        serializer_context = {
            "request": request,
        }

        if "id" in params:
            queryset = TypeDependence.objects.filter(id__in=params["id"].split(","))
            serializer = TypeDependenceSerializers(
                queryset, context=serializer_context, many=True
            )
            logger.debug("**retrieving housing dependencies **")
            return serializer.data

        queryset = TypeDependence.objects.all()
        serializer = TypeDependenceSerializers(queryset, many=True)
        return {"success": True, "payload": serializer.data}

    def create_dependancy(self, request, params={}, *args, **kwargs):
        """Create housing dependency."""
        serializer_context = {
            "request": request,
        }
        if isinstance(request.data, list):
            dependencies = request.data
            housing_dependency_objects = []
            for dependency in dependencies:
                serializer = TypeDependenceSerializers(
                    data=dependency, context=serializer_context
                )
                serializer.is_valid(raise_exception=True)
                housing_dependency_objects.append(serializer)
            saved_dependencies = [model.save() for model in housing_dependency_objects]
            serialized_dependencies = TypeDependenceSerializers(
                saved_dependencies, context=serializer_context, many=True
            )
            return {"success": True, "payload": serialized_dependencies.data}
        serializer = TypeDependenceSerializers(
            data=request.data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "payload": serializer.data}

    def update_dependancy(self, request, params={}, *args, **kwargs):
        """
         Update housing dependency.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        serializer_context = {
            "request": request,
        }
        if isinstance(request.data, list):
            dependencies = request.data
            dependency_objects = []
            for dependency in dependencies:
                instance = TypeDependence.objects.get(pk=params.get("id", None))
                serializer = TypeDependenceSerializers(
                    instance, data=dependency, context=serializer_context
                )
                serializer.is_valid(raise_exception=True)
                dependency_objects.append(serializer)
            saved_dependencies = [model.save() for model in dependency_objects]
            serializer = TypeDependenceSerializers(
                saved_dependencies, many=True, context=serializer_context
            )
            return {"success": True, "payload": serializer.data}
        instance = get_object_or_404(TypeDependence, pk=params.get("id", None))
        serializer = TypeDependenceSerializers(
            instance, data=request.data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "payload": serializer.data}

class StructureAppartmentViewSet(ActionAPIView):
    """StructureAppartement Actions viewset."""

    def get_structure(self, request, params={}, *args, **kwargs):
        """Get all  structure."""
        get_all_structure = StructureAppartement.objects.all()
        serialized_structure = StructureAppartmentSerializers(
            get_all_structure, many=True
        ).data
        return {"success": True, "payload": serialized_structure}
