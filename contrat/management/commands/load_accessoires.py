import logging
import re

import requests
import six
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from contrat.models import Accesoireloyer

LIST_ACCESSOIRES = [
    'CAUTION EAU',
    'CAUTION ELECTRICITE',
    'CAUTION PEINTURE',
    'FRAIS DE VIDANGE FOSSES SCEPTIQUES',
    'FRAIS DE RAMASSAGE DE DECHETS MENAGER',
    'FRAIS DE NETTOYAGE GENERAL',
]

logger = logging.getLogger(__name__)


def create_accessoires():
    """
    Insert each object in accessoire loyer list in according table if not exist
    :return: num_updated: int, num_created: int
    :raise ValidationError:
    """
    num_created = 0
    for acc in LIST_ACCESSOIRES:
        nb = Accesoireloyer.objects.filter(libelle=acc).count()
        if nb > 0:
            continue

        try:
            Accesoireloyer.objects.create(libelle=acc, utilite=acc)
            num_created = num_created + 1
        except ValidationError as e:
            logger.debug(f"error while creating accesoire: {e}")

    return num_created

class Command(BaseCommand):
    help = "Creer les accesoires loyers connus qui n'existent pas dans la base"

    def handle(self, *args, **options):
        num_created = create_accessoires()
        self.stdout.write(
            "Banque creer avec succès.  "
            "%s accessoire loyer were updated, %s accessoire loyer were created." % (0, num_created))
