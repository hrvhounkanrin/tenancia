import logging
import re

import requests
import six
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from appartement.models import TypeDependence

TYPE_DEPEDANCE = [
    'SEJOUR',
    'CUSINE',
    'CHAMBRE A COUCHER',
    'DOUCHE',
    'SALLE A MANGER',
    'ARRIERE COUR',
    'VERANDA',
    'BALCON',
    'TERRASSE'
]

logger = logging.getLogger(__name__)


def create_type_dependance():
    """
    Insert each object in type_dependance list in according table if not exist
    :return: num_updated: int, num_created: int
    :raise ValidationError:
    """
    num_created = 0
    for depency in TYPE_DEPEDANCE:
        nb = TypeDependence.objects.filter(libelle=depency).count()
        if nb > 0:
            continue

        try:
            TypeDependence.objects.create(libelle=depency, utilite=depency)
            num_created = num_created + 1
        except ValidationError as e:
            logger.debug(f"error while creating dependecy: {e}")

    return num_created

class Command(BaseCommand):
    help = "Creer les type de dependances connues qui n'existe pas dans la base"

    def handle(self, *args, **options):
        num_created = create_type_dependance()
        self.stdout.write(
            "Type de dependance creer avec succès.  "
            "%s dependency were updated, %s dependency were created." % (0, num_created))
