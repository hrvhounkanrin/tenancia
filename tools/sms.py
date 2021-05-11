import logging
import os

from django.conf import settings
from twilio.rest import Client

from contrat.models import Contrat
from meslimmo.celery import app

logger = logging.getLogger(__name__)

account_sid = os.environ.get("TWILIO_ACCOUNT_SID", settings.TWILIO_ACCOUNT_SID)
account_token = os.environ.get("TWILIO_AUTH_TOKEN", settings.TWILIO_AUTH_TOKEN)


class Sms:
    def __init__(self):
        pass

    @app.task(bind=True, name="sms.contrat_emis_sms")
    def contrat_emis_sms(self, contrat):
        client = Client(account_sid, account_token)
        first_name = contrat["first_name"]
        body = "Bonjour {}. Le contrat de bail n° {} d'un montant périodique de {}\
         a été émis sur votre compte. Connectez vous sur Tenancia pour valider avant le {}, date effet de ce contrat.".format(
            first_name,
            contrat["reference"],
            contrat["montant_bail"],
            contrat["date_effet"],
        )
        message = client.messages.create(
            to=contrat["phone_number"], from_="+13052904936", body=body
        )
        logger.debug(message)

    @app.task(bind=True, name="sms.contrat_valide_sms")
    def contrat_valide_sms(self, contrat_data):
        client = Client(account_sid, account_token)
        logger.debug(f"This is contrat_data: {contrat_data}")
        client_accord = "accepté" if contrat_data["client_accord"] is True else "refusé"
        body = "Bonjour {}. Le contrat n° {}, en date du {}, a été {} par le client {}".format(
            contrat_data["first_name"],
            contrat_data["reference"],
            contrat_data["created_at"],
            client_accord,
            contrat_data["client_name"],
        )
        message = client.messages.create(
            to=contrat_data["phone_number"], from_="+13052904936", body=body
        )
        logger.debug(message)

    @app.task(bind=True, name="sms.contrat_valide_sms")
    def contrat_valide_client_sms(self, quittances_data):
        logger.debug(quittances_data)
        client = Client(account_sid, account_token)
        body = "Bonjour {}. Vous venez de valider le contrat n° {}. Vous avez donc des quittances d'un cout global de {} à régler. Veuillez vous connecter sur Tenancia pour le règlement".format(
            quittances_data["first_name"],
            quittances_data["reference"],
            quittances_data["montant_global"],
        )
        message = client.messages.create(
            to=quittances_data["phone_number"], from_="+13052904936", body=body
        )
        logger.debug(message)

    @app.task(bind=True, name="sms.contrat_quittance_cree_sms")
    def contrat_quittance_cree_sms(self, quittances_data):
        logger.debug(quittances_data)
        client = Client(account_sid, account_token)
        for quittance in quittances_data:
            body = "Bonjour {}. Vous avez la quittance n° {} de votre contrat de location n° {}, d'un montant de {}, en attente de paiement. Veuillez vous connecter sur Tenancia pour le règlement".format(
                quittance["first_name"],
                quittance["reference_quittance"],
                quittance["reference_contrat"],
                quittance["montant_global"],
            )
            message = client.messages.create(
                to=quittance["phone_number"], from_="+13052904936", body=body
            )
            logger.debug(message)
