"""
email.py
Module for sending emails
make email async https://code.tutsplus.com/tutorials/using-celery-with-django-for-background-task-processing--cms-28732

"""
import logging
import os

from celery.decorators import task
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.template import TemplateDoesNotExist
from django.template.loader import get_template, render_to_string

from meslimmo.celery import app

logger = logging.getLogger(__name__)


def sending_email(receiver, subject, template_name, key):
    """
    Accepts the following  parameters: receiver,subject,template_name,key
    send the email/ return error message
    """
    try:
        logger.debug(key)
        message = get_template(template_name=template_name).render(key)
        send_mail(
            subject,
            "Hello from tenancia",
            "tenancia@tenancia.com",
            [receiver],
            html_message=message,
        )

    except Exception as exception:
        logger.debug(exception)
        print(exception)


class Email:
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
        template_name = "authentication/reset-password.html"
        receiver = user.email
        subject = "Resetting Your Password For " + settings.SITE_NAME
        key = {"first_name": user.username, "password_reset_url": token}
        sending_email(receiver, subject, template_name, key)

    @task(name="emails.activate_clipped_asset")
    def password_change_email(self, user):
        """
        Accepts the following  parameters: user
        Create the customized password change  email for that user
        """
        subject = "Password Reset Successfully"
        template_name = "authentication/reset-password-confirmation.html"
        receiver = user.email

        key = {"first_name": user.username}
        sending_email(receiver, subject, template_name, key)

    @task(bind=True, name="emails.signup_email")
    def sign_up_email(self, user):
        """
        Accepts the following  parameters: user
        Create the customized signUp email for that user
        """
        template_name = "registration/activate_account.html"
        receiver = user["email"]
        subject = "Please Confirm Your E-mail Address"
        key = {
            "first_name": user["first_name"],
            "site_url": "www.tenancia.com",
            "uid": user["uid"],
            "token": user["token"],
            "front_url": os.environ.get("FRONTEND"),
        }
        sending_email(receiver, subject, template_name, key)

    @task(name="sum_two_numbers")
    def add(x, y):
        return x + y


"""
https://code.tutsplus.com/tutorials/using-celery-with-django-for-background-task-processing--cms-28732
"""
