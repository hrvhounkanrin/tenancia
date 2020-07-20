from collections import OrderedDict
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework import serializers
from rest_framework.fields import empty
from countries_plus.models import Country

class CountrySerialier(serializers.ModelSerializer):
    """Country plus Model serializer."""

    class Meta:
        """Country model meta."""

        model = Country
        fields = '__all__'


class DictSerializer(serializers.ListSerializer):
    """
    Overrides default ListSerializer to return a dict with a custom field from
    each item as the key. Makes it easier to normalize the data so that there
    is minimal nesting. dict_key defaults to 'id' but can be overridden.
    """
    dict_key = 'id'

    @property
    def data(self):
        """
        Overriden to return a ReturnDict instead of a ReturnList.
        """
        ret = super(serializers.ListSerializer, self).data
        return ReturnDict(ret, serializer=self)

    def to_representation(self, data):
        """
        Converts the data from a list to a dictionary.
        """
        items = super(DictSerializer, self).to_representation(data)
        return {item[self.dict_key]: item for item in items}


class AsymetricRelatedField(serializers.PrimaryKeyRelatedField):

    # en lecture, je veux l'objet complet, pas juste l'id
    def to_representation(self, value):
        return self.serializer_class(value).data

    # petite astuce perso et pas obligatoire pour permettre de taper moins
    # de code: lui faire prendre le queryset du model du serializer
    # automatiquement. Je suis lazy
    def get_queryset(self):
        if self.queryset:
            return self.queryset
        return self.serializer_class.Meta.model.objects.all()

    # Get choices est utilisé par l'autodoc DRF et s'attend à ce que
    # to_representation() retourne un ID ce qui fait tout planter. On
    # réécrit le truc pour utiliser item.pk au lieu de to_representation()
    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([
            (
                item.pk,
                self.display_value(item)
            )
            for item in queryset
        ])

    # DRF saute certaines validations quand il n'y a que l'id, et comme ce
    # n'est pas le cas ici, tout plante. On désactive ça.
    def use_pk_only_optimization(self):
        return False

    # Un petit constructeur pour générer le field depuis un serializer. lazy,
    # lazy, lazy...
    @classmethod
    def from_serializer(cls, serializer, name=None, args=(), kwargs={}):
        if name is None:
            name = f"{serializer.__name__}AsymetricAutoField"

        return type(name, (cls,), {"serializer_class": serializer})



# https://www.erol.si/2015/09/django-rest-framework-nestedserializer-with-relation-and-crud/
class RelationModelSerializer(serializers.ModelSerializer):
    """Manage models relationships"""

    def __init__(self, instance=None, data=empty, **kwargs):
        self.is_relation = kwargs.pop('is_relation', False)
        super(RelationModelSerializer, self).__init__(instance, data, **kwargs)

    def validate_empty_values(self, data):
        if self.is_relation:
            model = getattr(self.Meta, 'model')
            model_pk = model._meta.pk.name

            if not isinstance(data, dict):
                error_message = self.default_error_messages['invalid'].format(datatype=type(data).__name__)
                raise serializers.ValidationError(error_message)

            if not model_pk in data:
                raise serializers.ValidationError({model_pk: model_pk + ' is required'})

            try:
                instance = model.objects.get(pk=data[model_pk])
                return True, instance
            except:
                raise serializers.ValidationError({model_pk: model_pk + ' is not valid'})

        return super(RelationModelSerializer, self).validate_empty_values(data)
