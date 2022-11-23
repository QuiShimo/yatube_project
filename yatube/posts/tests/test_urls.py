from django.test import TestCase, Client


class StaticURLTest(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_homepahe(self):
        response = self.guest_client.get('/')
        self.assertEquals(response.status_code, 200)
