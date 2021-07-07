from django.test import TestCase
from django.urls import reverse
from core.models import Subscribers
from django.test import Client
from majibu.settings import MAX_THROTTLE_REQUESTS


class IndexViewTest(TestCase):
    def test_index_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')


class ReservationViewTest(TestCase):
    def test_reservation_view_url_exists_at_desired_location(self):
        response = self.client.get('/reservation')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subscribe.html')

    def test_reservation_view_url_accessible_by_name(self):
        response = self.client.get(reverse('reservation'))
        self.assertEqual(response.status_code, 200)

    def test_reservation_view_redirects_to_correct_url(self):
        response = self.client.post(
            reverse('reservation'),
            data={
                'name': "John",
                'email': "johndoe@gmail.com"
                }
        )
        self.assertRedirects(response, '/info', status_code=302)

    def test_reservation_does_not_redirect_invalid_form(self):
        subscriber = Subscribers.objects.create(
            name='john doe', email='johndoe@gmail.com'
        )
        response = self.client.post(
            reverse('reservation'),
            data={
                'name': subscriber.name,
                'email': subscriber.email
                }
        )
        self.assertContains(response,  '*This email is already enrolled. Try another one!')

    def test_reservation_view_throttles_requests(self):
        client = Client()
        no_of_requests = int(MAX_THROTTLE_REQUESTS) + 1

        for r in range(0, no_of_requests):
            response = client.get(reverse('reservation'))

        self.assertEqual(response.status_code, 403)


class InfoViewTest(TestCase):
    def setUp(self):
        message = """
            Something is fishy about this email... Did you type you
            email address correctly?
        """
        session = self.client.session
        session['message'] = message
        session.save()

    def test_info_view_url_exists_at_desired_location(self):
        response = self.client.get('/info')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info.html')

    def test_info_view_url_accessible_by_name(self):
        response = self.client.get(reverse('info'))
        self.assertEqual(response.status_code, 200)

    def test_info_view_contains_message(self):
        response = self.client.get(reverse('info'))
        session = self.client.session
        self.assertContains(response,  session['message'])

    def test_info_view_redirects_invalid_message(self):
        self.client.session.delete()
        response = self.client.get(reverse('info'))

        self.assertRedirects(response, '/reservation', status_code=302)
