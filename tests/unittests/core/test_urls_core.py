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
    
    def test_userProfile_url(self):
        url = reverse("userProfile")
        self.assertEqual(resolve(url).func, userProfile)
    
    def test_menuType_url(self):
        url = reverse("menuType", args=(1,))
        self.assertEqual(resolve(url).func, menuType)
        
    def test_timeline_url(self):
        url = reverse("timeline")
        self.assertEqual(resolve(url).func, timeline)
