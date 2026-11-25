from django.test import TestCase, Client

class SimpleTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_endpoint_without_token(self):
        response = self.client.get("/api/habit/all/")
        self.assertEqual(response.status_code, 401)