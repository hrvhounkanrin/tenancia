"""
Module for sending emails
make email async https://code.tutsplus.com/tutorials/using-celery-with-django-for-background-task-processing--cms-28732

"""
import logging
from django.template.loader import get_template
from django.conf import settings

from django.core.mail import EmailMessage
from django.template import TemplateDoesNotExist

from meslimmo.celery import app
logger = logging.getLogger(__name__)

class Email():
    """
    This class is responsible for sending customized emails.
    """

    def __init__(self):
        pass

    def forget_password_email(self, user, token):
        """
        Accepts the following  parameters: user , token
        Create the customized forget password email for that user
        """
        template_name = 'authentication/reset-password.html'
        receiver = user.email
        subject = 'Resetting Your Password For ' + settings.SITE_NAME
        key = {
            'first_name': user.username,
            'password_reset_url': token
        }
        self.send_email(receiver, subject, template_name, key)

    @app.task(name='emails.activate_clipped_asset')
    def password_change_email(self, user):
        """
        Accepts the following  parameters: user
        Create the customized password change  email for that user
        """
        subject = 'Password Reset Successfully'
        template_name = 'authentication/reset-password-confirmation.html'
        receiver = user.email

        key = {
            'first_name': user.username
        }
        self.send_email(receiver, subject, template_name, key)

    # @app.task(bind=True, name='emails.signup_email')
    def sign_up_email(self, user):
        """
        Accepts the following  parameters: user
        Create the customized signUp email for that user
        """
        template_name = 'authentication/confirmation-email.html'
        receiver = user['email']
        subject = 'Please Confirm Your E-mail Address'
        key = {
            'first_name': user['first_name'],
            'site_url': 'www.tenancia.com'
        }

        self.send_email(receiver, subject, template_name, key)

    @staticmethod
    def send_email(receiver, subject, template_name, key):
        logger.info('start send_email ok')
        """
        Accepts the following  parameters: receiver,subject,template_name,key
        send the email/ return error message
        """
        try:
            print('start mail send ok')
            message = get_template(template_name=template_name).render(key)
            email = EmailMessage(subject, message, to=[receiver])
            email.content_subtype = 'html'
            email.send()

        except Exception as exception:
            logger.debug(exception)
            print(exception)


'''
https://code.tutsplus.com/tutorials/using-celery-with-django-for-background-task-processing--cms-28732
'''