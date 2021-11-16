# coding=utf-8
import logging
import re

import requests
import six
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


def parse_geonames_data():
    """
    Insert each object in type_dependance list in according table if not exist
    :return: num_updated: int, num_created: int
    :raise ValidationError:
    """
    num_created = 0
    num_updated = 0
    for depency in TYPE_DEPEDANCE:
        nb = TypeDependence.objects.filter(libelle==depency).count()
        if nb > 0:
            continue

        try:
            TypeDependence.obects.create(libelle=depency, utilite=depency)
            num_created = num_created+1
        except ValidationError as e:
           logger.debug(f"error while creating dependecy: {e}")

    return num_updated, num_created
