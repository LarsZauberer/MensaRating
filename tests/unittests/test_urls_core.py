from django.test import SimpleTestCase
from django.urls import reverse, resolve
from core.views import index, app


class TestUrlsIndex(SimpleTestCase):
    def test_index_url(self):
        url = reverse("index")
        self.assertEqual(resolve(url).func, index)
        
    def test_app_url(self):
        url = reverse("app")
        self.assertEqual(resolve(url).func, app)
