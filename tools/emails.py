"""
Module for sending emails
make email async https://code.tutsplus.com/tutorials/using-celery-with-django-for-background-task-processing--cms-28732

"""
import logging
import os
from celery.decorators import task
from django.template import Context
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from email.mime.image import MIMEImage
from django.template.loader import get_template, render_to_string

from meslimmo.celery import app

logger = logging.getLogger(__name__)

"""
def make_activation_code():
    random_string = str(random.random())
    random_digest = sha1(force_bytes(random_string)).hexdigest()[:5]
    time_string = str(datetime.now().microsecond)

    combined_string = random_digest + time_string

    return sha1(force_bytes(combined_string)).hexdigest()
"""

def sending_email(receiver, subject, template_name, key):
    """
    Accepts the following  parameters: receiver,subject,template_name,key
    send the email/ return error message
    """
    try:
        logger.debug(f"key_data: {key}")
        message = get_template(template_name=template_name).render(key)
        msg = EmailMultiAlternatives(subject, body=message, from_email="Hello from tenancia", to=[receiver])
        msg.content_subtype = "html"
        msg.mixed_subtype = "related"

        """
        img_dir = 'static/mail'
        img_names = ['facebook.png', 'instagram.png', 'linkedin.png', 'mail.png', 'mail-separator.png', 'tenancia.png', 'youtube.png']
        for img_name in img_names:
            file_path = os.path.join(img_dir, img_name)
            with open(file_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-ID', '<{name}>'.format(name=img_name))
                img.add_header('Content-Disposition', 'inline', filename=img_name)
            msg.attach(img)
            logger.info('<{name}>'.format(name=img_name))
        """
        msg.send(fail_silently=False)
        logger.info(f"Activation mail sent to {receiver} with {key} as data")
        """
        send_mail(
            subject,
            "Hello from tenancia",
            "tenancia@tenancia.com",
            [receiver],
            html_message=message,
        )
        """

    except Exception as exception:
        logger.debug(f"Error occured: {exception}")
        print("Error occured")
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



"""
https://code.tutsplus.com/tutorials/using-celery-with-django-for-background-task-processing--cms-28732
"""
