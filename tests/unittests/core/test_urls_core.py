from django.test import SimpleTestCase
from django.urls import reverse, resolve
from core.views import *


class TestUrlsIndex(SimpleTestCase):
    def test_index_url(self):
        url = reverse("index")
        self.assertEqual(resolve(url).func, index)
        
    def test_menu_url(self):
        url = reverse("menu", args=(1,))
        self.assertEqual(resolve(url).func, menu)
        
    def test_allMenu_url(self):
        url = reverse("allMenu")
        self.assertEqual(resolve(url).func, allMenu)
