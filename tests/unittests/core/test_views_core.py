from django.test import TestCase, Client
from django.urls import reverse
from core.models import Menu, Review, Image, Rating
from django.contrib.auth import User


class TestViewsCore(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='user')

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

    def test_postReview_no_login(self):
        # Create Menu instance
        menu = Menu.objects.create(name="Test Menu", description="Test")

        client = Client()
        response = client.post(reverse("postReview", args=(1,)), data={"text": "Test Text"})

        self.assertEqual(response.status_code, 200)
        
        # Get review object from the database
        review = Review.objects.get(pk=1)
        self.assertEqual(review.menu, menu)
        self.assertEqual(review.profil, None)
        self.assertEqual(review.likes, 0)
        self.assertEqual(review.text, "Test")
    
    def test_postReview_login(self):
        # Create Menu instance
        menu = Menu.objects.create(name="Test Menu", description="Test")

        client = Client()
        client.login(username="user", password="user")
        response = client.post(reverse("postReview", args=(1,)), data={"text": "Test Text"})

        self.assertEqual(response.status_code, 200)
        
        # Get review object from the database
        review = Review.objects.get(pk=1)
        self.assertEqual(review.menu, menu)
        self.assertEqual(review.profil, self.user)
        self.assertEqual(review.likes, 0)
        self.assertEqual(review.text, "Test")

    def test_postImage_get(self):
        # Create Menu instance
        menu = Menu.objects.create(name="Test Menu", description="Test")
        
        client = Client()
        response = client.get(reverse("postImage", args=(1,)))

        # TODO: Implement
        pass

    def test_postRating_no_login_valid(self):
        # Create Menu instance
        menu = Menu.objects.create(name="Test Menu", description="Test")
        
        client = Client()
        response = client.post(reverse("postRating", args=(1,)), data={"rating": 6})

        self.assertEqual(response.status_code, 200)
        
        # Get review object from the database
        rating = Rating.objects.get(pk=1)
        self.assertEqual(rating.menu, menu)
        self.assertEqual(rating.profil, None)
        self.assertEqual(rating.rating, 6)
    
    def test_postRating_login_valid(self):
        # Create Menu instance
        menu = Menu.objects.create(name="Test Menu", description="Test")
        
        client = Client()
        client.login(username="user", password="user")
        response = client.post(reverse("postRating", args=(1,)), data={"rating": 6})

        self.assertEqual(response.status_code, 200)
        
        # Get review object from the database
        rating = Rating.objects.get(pk=1)
        self.assertEqual(rating.menu, menu)
        self.assertEqual(rating.profil, self.user)
        self.assertEqual(rating.rating, 6)
    
    def test_postRating_no_login_invalid(self):
        # Create Menu instance
        menu = Menu.objects.create(name="Test Menu", description="Test")
        
        client = Client()
        response = client.post(reverse("postRating", args=(1,)), data={"rating": 7})

        self.assertEqual(response.status_code, 200)
        
        self.assertEquals(response.content, "Invalid")
        
    def test_postRating_login_change(self):
        # Create Menu instance
        menu = Menu.objects.create(name="Test Menu", description="Test")
        
        client = Client()
        client.login(username="user", password="user")
        response = client.post(reverse("postRating", args=(1,)), data={"rating": 6})
        response = client.post(reverse("postRating", args=(1,)), data={"rating": 5})

        self.assertEqual(response.status_code, 200)
        
        # Get review object from the database
        rating = Rating.objects.get(pk=1)
        self.assertEqual(rating.menu, menu)
        self.assertEqual(rating.profil, self.user)
        self.assertEqual(rating.rating, 5)
