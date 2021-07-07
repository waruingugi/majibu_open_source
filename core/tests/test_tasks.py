from django.test import TestCase
from core.tasks import (
    email_validity_check, generate_names
)
from unittest.mock import Mock
import core.tasks as tasks  # noqa
import os
import smtplib
import ssl


class EmailValidityTest(TestCase):
    def test_email_is_valid(self):
        email = 'johdoe@gmail.com'
        validity = email_validity_check(email)
        self.assertTrue(validity)

    def test_email_is_invalid(self):
        email = 'johdoe@mailnator.com'
        validity = email_validity_check(email)
        self.assertFalse(validity)


class GenerateNamesTest(TestCase):
    def test_length_of_data(self):
        names, no_of_names = generate_names()
        self.assertEquals(30, len(names))
        self.assertEquals(no_of_names, len(names))

    def test_names_and_time_in_data(self):
        names, no_of_names = generate_names()
        self.assertEquals({'name', 'time'}, names[0].keys())
        self.assertEquals({'name', 'time'}, names[29].keys())


class SendMailTest(TestCase):
    def setUp(self):
        self.sender_email = os.environ['SENDER_EMAIL']
        self.send_email_password = os.environ['SENDER_EMAIL_PASSWORD']
        self.port = os.environ['SENDER_EMAIL_SMTP_SERVER_OUTGOING_PORT']
        self.smtp_server = os.environ['SENDER_EMAIL_SMTP_SERVER']

    def test_send_mail(self):
        receiver_name = 'john'
        receiver = 'johndoe@gmail.com'

        tasks = Mock()  # noqa
        tasks.send_mail(receiver, receiver_name)
        tasks.send_mail.assert_called_once_with(receiver, receiver_name)

    def test_send_mail_keys_exist(self):
        self.assertIsNotNone(self.sender_email)
        self.assertIsNotNone(self.send_email_password)
        self.assertIsNotNone(self.smtp_server)
        self.assertIsNotNone(self.port)

    def test_can_login_with_send_mail_keys(self):
        context = ssl.create_default_context()
        server = smtplib.SMTP(self.smtp_server, self.port)
        server.starttls(context=context)

        response = server.login(self.sender_email, self.send_email_password)
        self.assertEquals(response[0], 235)
