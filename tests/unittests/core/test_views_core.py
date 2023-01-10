from django.test import TestCase, Client
from django.urls import reverse
from core.models import Menu, MenuType, Profil
from django.contrib.auth.models import User


class TestViewsCore(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='user')
        self.user_profil = Profil.objects.create(user=self.user)

    def test_index_get(self):
        client = Client()
        response = client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_menu_get(self):
        client = Client()

        # Create Menu instance
        menu = Menu.objects.create(name="Test Menu", description="Test", menuType=MenuType.objects.create(name="Test Menu"))

        response = client.get(reverse("menu", args=(menu.pk,)))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "menu.html")

    def test_allMenu_get(self):
        client = Client()
        response = client.get(reverse("allMenu"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "allMenu.html")

    def test_postReview_get(self):
        client = Client()
        # response = client.get(reverse("postReview", args=(1,)))

        # TODO: Implement
        pass

    def test_postImage_get(self):
        client = Client()
        # response = client.get(reverse("postImage", args=(1,)))

        # TODO: Implement
        pass

    def test_postRating_get(self):
        client = Client()
        # response = client.get(reverse("postRating", args=(1,)))

        # TODO: Implement
        pass
    
    def test_userProfile_get_no_login(self):
        client = Client()
        
        response = client.get(reverse("userProfile"))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
    
    def test_userProfile_get_login(self):
        client = Client()
        
        client.login(username='user', password='user')
        response = client.get(reverse("userProfile"))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "userProfile.html")

    def test_menuType_get(self):
        client = Client()
        
        menu = Menu.objects.create(name="Test Menu", description="Test", menuType=MenuType.objects.create(name="Test Menu"))
        
        response = client.get(reverse("menuType", args=(menu.menuType.pk,)))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "menuType.html")
    
    def test_timeline_get(self):
        client = Client()
        
        response = client.get(reverse("timeline"))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "timeline.html")
