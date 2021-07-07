from django.test import TestCase
from core.models import Subscribers
from authentication.models import User


class SubscribersTestCase(TestCase):
    def setUp(self):
        Subscribers.objects.create(
            name='john doe', email='johndoe@gmail.com'
        )

    def test_field_names_are_valid(self):
        email = Subscribers._meta.get_field('email').name
        name = Subscribers._meta.get_field('name').name
        subscribed_date = Subscribers._meta.get_field('subscribed_date').name

        self.assertEquals(name, 'name')
        self.assertEquals(email, 'email')
        self.assertEquals(subscribed_date, 'subscribed_date')

    def test_fields_are_not_empty(self):
        john_doe = Subscribers.objects.get(name='john doe')

        self.assertIsNotNone(john_doe.email)
        self.assertIsNotNone(john_doe.subscribed_date)

    def test_get_first_name(self):
        subscriber = Subscribers.objects.get(name='john doe')
        self.assertEquals('John', subscriber.first_name)
        self.assertEqual(subscriber.__unicode__(), subscriber.first_name)

    def test_subscribers_creation(self):
        subscriber = Subscribers.objects.get(name='john doe')
        self.assertEqual(subscriber.__str__(), subscriber.name)
