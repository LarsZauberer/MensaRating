from django.test import TestCase, Client
from django.urls import reverse


class TestViewsIndex(TestCase):
    def setUp(self):
        pass
    
    def test_index_get(self):
        client = Client()
        response = client.get(reverse("index"))
        
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, "index.html")
    
    def test_app_get(self):
        client = Client()
        response = client.get(reverse("app"))
        
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, "app.html")
