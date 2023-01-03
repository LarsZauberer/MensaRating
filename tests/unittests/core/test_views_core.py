from django.test import TestCase, Client
from django.urls import reverse
from core.models import Menu


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

        # Create Menu instance
        menu = Menu.objects.create(name="Test Menu", description="Test")

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
