"""Rest_graph_ql app serializer.."""
from rest_framework import serializers


class GenericModelSerializer(serializers.ModelSerializer):
    """Generic model serializer."""

    """
    A ModelSerializer that takes additional
     'fields' and 'model_class' arguments that
    controls which fields should be displayed.
    """

    class Meta:
        """GenericModelSerializer meta."""

        model = None
        fields = []

    def __init__(self, *args, **kwargs):
        """Model serializer  init."""
        fields = kwargs.pop("fields", None)
        model = kwargs.pop("model_class", None)
        if fields is not None:
            self.Meta.fields = fields
        if model is not None:
            self.Meta.model = model
            if fields is None:
                fields = [item.name for item in model._meta.fields]
        super(GenericModelSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            self.Meta.fields = fields
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class FieldMixin(object):
    """Turning to mixin / This class maybe extended."""

    # TODO : TO be customized fully---> then make it more usable
    def get_fields_names(self, *args, **kwargs):
        """
        Get field names.

        :param args:
        :param kwargs:
        :return:
        """
        fields_names = self.context.get("fields", None)
        if fields_names:
            return fields_names
        return super(FieldMixin, self).get_fields_names(*args, **kwargs)


class APISerializer(serializers.BaseSerializer):
    """APISerializer."""

    def to_representation(self, data):
        """To representation."""
        success = True
        payload = data
        if isinstance(data, dict):
            if "success" in data:
                success = data.pop("success")
            if "payload" in data:
                payload = data.pop("payload")
            if "reason" in data:
                reason = data.get("reason")
                self.context["reason"] = reason
        self.context["success"] = success

        return dict(self.context, **{"payload": payload})
