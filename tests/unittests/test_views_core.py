from django.test import TestCase, Client
from django.urls import reverse


class TestViewsCore(TestCase):
    def setUp(self):
        pass
    
    def test_index_get(self):
        client = Client()
        response = client.get(reverse("index"))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
    
    def test_menu_get(self):
        client = Client()
        response = client.get(reverse("menu"))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "menu.html")
        
    def test_allMenu_get(self):
        client = Client()
        response = client.get(reverse("allMenu"))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "allMenu.html")
