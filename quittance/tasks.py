import logging
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.utils.crypto import get_random_string
from contrat.models import Contrat
from quittance.models import Quittance
from calendar import monthrange
from tools.sms import Sms
from meslimmo.celery import app
logger = logging.getLogger(__name__)


def last_day_of_month(date_value):
    return date_value.replace(day=monthrange(date_value.year, date_value.month)[1])
@app.task(name='tasks.get_contrat_en_cours')
def get_contrat_en_cours():
    """Récupérer les contrats en cours dont la prochaine échéance est du jour"""
    logger.debug('start task ok')
    today = datetime.today()
    contrats = Contrat.objects.filter(prochaine_echeance=today, statut='EN COURS')
    logger.debug(contrats)
    quittances = []
    for contrat in contrats:
        date_valeur = datetime.today()
        sart_of_month = date_valeur.replace(day=1)
        end_of_month = last_day_of_month(sart_of_month)
        quittance = Quittance(reference=get_random_string(8).upper(), date_emission=datetime.today(),
                                      date_valeur=date_valeur, debut_periode=sart_of_month,
                                      fin_periode=end_of_month, nature='QUITTANCE DE LOYER',
                                      contrat=contrat, montant=contrat.montant_bail)
        prochaine_echeance = date(sart_of_month.year, sart_of_month.month, \
                                  contrat.jour_emission) + relativedelta(months=+1)
        contrat.prochaine_echeance = prochaine_echeance
        quittances.append(quittance)
    [quittance.save() for quittance in quittances ]
    # maj des prochaine echeances
    [contrat.save() for contrat in contrats]

    quittances_msg = []
    for quittance in quittances:
        quittance_msg = {
            'first_name': quittance.contrat.client.user.first_name,
            'reference_quittance': quittance.reference,
            'reference_contrat': quittance.contrat.reference_bail,
            'montant_global': quittance.montant,
            'phone_number': quittance.contrat.client.user.phone_number,
        }
        quittances_msg.append(quittance_msg)
    sms = Sms()
    sms.contrat_quittance_cree_sms.delay(quittances_msg)

