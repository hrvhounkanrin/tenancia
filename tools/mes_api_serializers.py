from rest_framework import serializers

# Le but est de creer une architecture simple a comprendre  et en mettant  securisee, flexible et bcp plus automatisee pour  la base de tout les services quon ecrira
#Il y aura  ci dessus 2 classes importantes une pour  nos serializers de facon plus diversiee et une auttre pour les serializers generique
#Toute fois les serializers generiques ne seront pas  100% utilise vu quon ne suivra la norme rest toute les fois

""" READY LET US GO """
class APISerializer(serializers.BaseSerializer):
    """ Notre class APi Serializer herite de la baseSerializer classe"""
    
    def to_representation(self, data):
        success = True
        payload = data
        if isinstance(data, dict):
            if 'success' in data:
                success = data.pop('success')
            if 'payload' in data:
                payload = data.pop('payload')
            if 'reason' in data:
                reason = data.get('reason')
                self.context['reason'] = reason
        self.context['success'] = success

        return dict(self.context, **{
            'payload': payload
        })



class GenericModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes additional `fields` and `model_class` arguments that
    controls which fields should be displayed.
    """
    class Meta:
        model = None
        fields = []


    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        # print fields
        # Don't pass the 'model_class' arg up to the superclass
        model = kwargs.pop('model_class', None)
        if fields is not None:
            self.Meta.fields = fields
        if model is not None:
            self.Meta.model = model
            if fields is None:
                fields = [item.name for item in model._meta.fields]

        # Instantiate the superclass normally
        super(GenericModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # print(fields)
            self.Meta.fields = fields
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class FieldMixin(object):
    """
       Turning to mixin / This class maybe extended to futureproofing stuffs/
       Can override the get_fields_names to get a specific field on our serializer

    """
    # TODO : TO be customized fully---> then make it more usable

    def get_fields_names(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        fields_names = self.context.get('fields', None)
        if fields_names:
            return fields_names
        return super(FieldMixin, self).get_fields_names(*args, **kwargs)

