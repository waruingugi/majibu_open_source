from django.test import TestCase
from core.forms import SubscribersForm
from core.models import Subscribers


class SubscriberFormTest(TestCase):
    def test_form_is_valid(self):
        form_data = {
            'name': 'John doe',
            'email': 'johndoe@gmail.com',
        }
        form = SubscribersForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_email_is_invalid(self):
        form_data = {
            'name': 'John doe',
            'email': '',
        }
        form = SubscribersForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_name_is_invalid(self):
        form_data = {
            'name': '',
            'email': 'johndoe@gmail.com',
        }
        form = SubscribersForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_user_exists(self):
        subscriber = Subscribers.objects.create(
            name='john doe', email='johndoe@gmail.com'
        )
        form_data = {
            'name': subscriber.name,
            'email': subscriber.email,
        }
        form = SubscribersForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('email'))
