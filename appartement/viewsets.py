from rest_framework.response import Response
from rest_framework import exceptions, status
from appartement.serializers import ( AppartementSerializers, StructureAppartmentSerializers, ComposantAppartmentSerializers,)
from appartement.models import (Appartement, ComposantAppartement, StructureAppartement, )
from rest_framework import views, viewsets, authentication, permissions, mixins, pagination
from tools.viewsets import ActionAPIView

class AppartementViewSet(ActionAPIView):
    def get_appartment(self, request, params ={} , *args, **kwargs):
        """  Get all  appartements """
        get_all_appartment = Appartement.objects.all()
        serialized_appartment = AppartementSerializers(get_all_appartment, many=True).data
        return {"success": True, "appartements": serialized_appartment}
    get_appartment.__doc__ = "  Get all  appartements "

    def get_building_appartment(self, request, params={}, *args, **kwargs):
        pass

    def create_appartment(self, request, params={}, *args, **kwargs):
        """Create appartment"""
        serialized_appartment = AppartementSerializers(data=request.data)
        if(serialized_appartment.is_valid()):
            serialized_appartment.save()
        return Response(serialized_appartment.data, status=status.HTTP_201_CREATED)
        create_appartment.__doc__="Create appartment"



class ComposantAppartementViewSet(ActionAPIView):
    def get_component(self, request, params ={} , *args, **kwargs):
        """  Get all avavaible appartement component whatever the language"""
        get_all_appartment_component = ComposantAppartement.objects.all()
        serialized_component = ComposantAppartmentSerializers(get_all_appartment_component, many=True).data
        return {"success": True, "composantAppartements": serialized_component}
        get_component.__doc__ =  "The simple way to get the list of all the appartment component using the APIActionViewSet"

    """
    Le premier create_component que j'ai écrit
    def create_component(self, request, params={}, *args, **kwargs):
        serialized_component = ComposantAppartmentSerializers(data=request.data)
        if serialized_component.is_valid():
            serialized_component.save()
            return Response(serialized_component.data, status=status.HTTP_201_CREATED)
        return Response(serialized_component._errors, status=status.HTTP_400_BAD_REQUEST)
    """

    """
    def create_component(self, request, params={}, *args, **kwargs):
        #This request should return only newly objects(those in request.data object). Not the whole
        #Le second problème c'est que la requête n'est pas atomique
       
        composant_appart = ComposantAppartement.objects.all()
        for composant_appartement in params['composant_appartement']:
            lib_ = composant_appartement['libelle']
            util_ = composant_appartement['utilite']
            create_appart = ComposantAppartement.objects.create(
                libelle=lib_,
                utilite=util_
            )
        create_appart =ComposantAppartmentSerializers(composant_appart, many=True).data
        return {"success": True, "composant_apart": create_appart}
    """
    def create_component(self, request, params={}, *args, **kwargs):
        """  Create an appartment component, it take a single component or a list of components"""
        #When request.data content a list of objects
        if isinstance(request.data.get('composant_appartement', None), list):
            composants = request.data.pop('composant_appartement')
            aappartment_component_objects = []
            for composant in composants:
                # validate each model with one seat at a time
                serializer = ComposantAppartmentSerializers(data=composant)
                serializer.is_valid(raise_exception=True)
                aappartment_component_objects.append(serializer)
            # Save all validated models in bloc
            saved_components = [model.save() for model in aappartment_component_objects]
            serialized_composants = ComposantAppartmentSerializers(saved_components, many=True)
            return {"success": True, "composant_apart": serialized_composants.data}
        #when request.data content single object
        serializer = ComposantAppartmentSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "composant_apart": serializer.data}


class StructureAppartmentViewSet(ActionAPIView):
    def get_structure(self, request, params ={} , *args, **kwargs):
        """  Get all  structure """
        get_all_structure = StructureAppartement.objects.all()
        serialized_structure = StructureAppartmentSerializers(get_all_structure, many=True).data
        return {"success": True, "structures": serialized_structure}
        get_structure.__doc__ = "  Get all  structure "