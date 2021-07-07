import requests
import os
from core.sub_logger import logger
import names
import random

# Email modules
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from string import Template

from majibu.settings import BASE_DIR
from os import path
from celery import shared_task
from core.templates.email_templates.email_one import plain_text_email


def email_validity_check(email_address):
    # Default variable for email_validity
    valid_email = True
    try:
        url = "https://mailcheck.p.rapidapi.com/"
        querystring = {"domain": email_address}

        headers = {
            'x-rapidapi-host': "mailcheck.p.rapidapi.com",
            'x-rapidapi-key': os.environ['MAIL_CHECK_KEY']
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        response = response.json()

        risk = response['risk']
        disposable = response['disposable']

        if (risk > 48) or (disposable is True):
            valid_email = False
            logger.info("email_validity_check Task: {} is risky.".format(email_address))
        else:
            valid_email = True
            logger.info("email_validity_check Task: {} is not risky.".format(email_address))

    except Exception as e:
        logger.error("email_validity_check: {}".format(e.__class__))
    finally:
        return valid_email


def generate_names():
    dummy_subscribers = []

    # Generate random names
    random_names = []
    for r in range(0, 100):
        random_names.append(names.get_first_name())

    all_names = random_names
    random.shuffle(all_names)
    selected_names = all_names[:30]

    for name in selected_names:
        minutes_ago = random.randint(3, 55)
        hours_ago = random.randint(1, 23)
        days_ago = random.randint(1, 4)

        # M - minutes, H - hours, D - days
        random_time = ['M', 'H', 'D']
        selected_time = random.choice(random_time)

        if selected_time == 'M':
            time = str(minutes_ago) + " minutes ago"
            dummy_subscribers.append(
                {"name": name, "time": time}
            )

        elif selected_time == 'H':
            if hours_ago > 1:
                time = str(hours_ago) + " hours ago"
            else:
                time = str(hours_ago) + " hour ago"

            dummy_subscribers.append(
                {"name": name, "time": time}
            )

        else:
            if days_ago > 1:
                time = str(days_ago) + " days ago"
            else:
                time = str(days_ago) + " day ago"

            dummy_subscribers.append(
                {"name": name, "time": time}
            )

    no_of_dummy_subscribers = len(dummy_subscribers)

    logger.info("generate_names Task: Generated names successfully.")
    return dummy_subscribers, no_of_dummy_subscribers


def send_mail(receiver, receiver_name):
    logger.info("send_mail Task: Start of Execution.")
    receiver_email = receiver

    sender_email = os.environ['SENDER_EMAIL']
    from_sender_email = os.environ['FROM_SENDER_EMAIL']
    send_email_password = os.environ['SENDER_EMAIL_PASSWORD']

    message = MIMEMultipart("alternative")
    message["Subject"] = "Congratulations {}! One last thing.".format(receiver_name)
    message["From"] = from_sender_email
    message["To"] = receiver_email

    """
    Returns a Template object comprising the contents of the
    file specified by filename.
    """
    email_template_dir = path.join(BASE_DIR, 'core/templates/email_templates').replace('\\', '/')
    email_template_html = path.join(email_template_dir, 'email_one.html').replace('\\', '/')
    email_template_text = plain_text_email

    with open(email_template_html, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
        email_template_html = template_file_content
        logger.info("send_mail Task: HTML Email template retrieved successfully.")

    email_template_html = Template(email_template_html).safe_substitute(
        name=receiver_name
    )

    email_template_text = plain_text_email.format(name=receiver_name)

    # Turn these into plain/html MIMEText objects
    basic_message = MIMEText(email_template_text, "plain")
    html_message = MIMEText(email_template_html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(basic_message)
    message.attach(html_message)

    smtp_server = os.environ['SENDER_EMAIL_SMTP_SERVER']
    context = ssl.create_default_context()
    port = os.environ['SENDER_EMAIL_SMTP_SERVER_OUTGOING_PORT']

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            logger.info("send_mail Task: Initiating connection to send mail server.")
            server.ehlo()  # Can be omitted
            server.starttls(context=context)

            server.ehlo()  # Can be omitted
            server.login(sender_email, send_email_password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

            logger.info("send_mail Task: Email sent successfully to {}.".format(receiver_email))
    except Exception as e:
        logger.error("send_mail Task: {}".format(e.__class__))


@shared_task(name="send_welcome_email_task")
def send_welcome_email_task(email, name):
    """Sends an email when a user enrolls."""
    return send_mail(email, name)
