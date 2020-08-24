# -*- coding: UTF-8 -*-
"""Misc serializers."""
from collections import OrderedDict
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework import serializers
from countries_plus.models import Country


class CountrySerialier(serializers.ModelSerializer):
    """Country plus Model serializer."""

    class Meta:
        """Country model meta."""

        model = Country
        fields = '__all__'


class DictSerializer(serializers.ListSerializer):
    """
    Override default ListSerializer to return a dict.

    with a custom field from each item as the key.
    Makes it easier to normalize the data so that there
    is minimal nesting. dict_key defaults to 'id' but can be overridden.
    """

    dict_key = 'id'

    @property
    def data(self):
        """Overriden to return a ReturnDict instead of a ReturnList."""
        ret = super(serializers.ListSerializer, self).data
        return ReturnDict(ret, serializer=self)

    def to_representation(self, data):
        """Convert the data from a list to a dictionary."""
        items = super(DictSerializer, self).to_representation(data)
        return {item[self.dict_key]: item for item in items}


class AsymetricRelatedField(serializers.PrimaryKeyRelatedField):
    """Récupéreration de données assymétriques."""

    def to_representation(self, value):
        """I really don't know what this function ain to."""
        return self.serializer_class(value).data

    def get_queryset(self):
        """I really don't know what this function ain to."""
        if self.queryset:
            return self.queryset
        return self.serializer_class.Meta.model.objects.all()

    def get_choices(self, cutoff=None):
        """I really don't know what this function ain to."""
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

    def use_pk_only_optimization(self):
        """I really don't know what this function ain to."""
        return False

    @classmethod
    def from_serializer(cls, serializer, name=None, args=(), kwargs={}):
        """I really don't know what this function ain to."""
        if name is None:
            name = f"{serializer.__name__}AsymetricAutoField"

        return type(name, (cls,), {"serializer_class": serializer})
