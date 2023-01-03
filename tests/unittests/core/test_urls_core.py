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
    
    def test_postReview_url(self):
        url = reverse("postReview", args=(1,))
        self.assertEqual(resolve(url).func, postReview)
    
    def test_postImage_url(self):
        url = reverse("postImage", args=(1,))
        self.assertEqual(resolve(url).func, postImage)
    
    def test_postRating_url(self):
        url = reverse("postRating", args=(1,))
        self.assertEqual(resolve(url).func, postRating)
