import logging
import re

import requests
import six
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from banque.models import Banque
from countries_plus.models import Country
LIST_BANK = [
    ('115', '115', 'BAB', 'BJ'),
    ('157', '157', 'BGFI', 'BJ'),
    ('1200', '1200', 'BHB', 'BJ'),
    ('300', '300', 'BIBE', 'BJ'),
    ('061', '061', 'BOA', 'BJ'),
    ('177', '177', 'CBAO', 'BJ'),
    ('212', '212', 'CORIS BANK', 'BJ'),
    ('062', '062', 'ECOBANK', 'BJ'),
    ('099', '099', 'NSIA BANK', 'BJ'),
    ('058', '058', 'ORABANK BENIN', 'BJ'),
    ('067', '067', 'UBA', 'BJ'),
    ('MOOVBENIN', 'MOOVBENIN', 'MOOV AFRICA', 'BJ'),
    ('MTNBENIN', 'MTNBENIN', 'MTN MOMO', 'BJ'),
]

logger = logging.getLogger(__name__)


def create_banks():
    """
    Insert each object in type_dependance list in according table if not exist
    :return: num_updated: int, num_created: int
    :raise ValidationError:
    """
    country = Country.objects.filter(iso='BJ').first()
    num_created = 0
    for bank in LIST_BANK:
        nb = Banque.objects.filter(codebanque=bank[0]).count()
        if nb > 0:
            continue

        try:
            Banque.objects.create(codebanque=bank[0], code_swift=bank[1], libbanque=bank[2], pays=country)
            num_created = num_created + 1
        except ValidationError as e:
            logger.debug(f"error while creating bank: {e}")

    return num_created

class Command(BaseCommand):
    help = "Creer les banques connus qui n'existent pas dans la base"

    def handle(self, *args, **options):
        num_created = create_banks()
        self.stdout.write(
            "Banque creer avec succès.  "
            "%s bank were updated, %s banks were created." % (0, num_created))
