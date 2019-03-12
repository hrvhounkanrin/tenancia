from rest_framework import serializers , exceptions

from . models import *

class ProprietaireSerializers(serializers.ModelSerializer):
    """
       Serializer for class proprietaire
    """
    immeubles = serializers.SerializerMethodField()
    class Meta:
        model = Proprietaire
        fields = ['mode_paiement','numcompte','user', 'banque', 'pays_residence', 'immeubles']

    def get_immeubles(self, blog):
        comments = Comment.objects.filter(
            post__blog=blog,
        )
        return CommentSerializer(
            comments,
            many=True,
            context={'request': self.context['request']}
        ).data