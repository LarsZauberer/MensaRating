from django.test import TestCase, Client
from django.urls import reverse
from core.models import Menu, Review, Image, Rating, Profil
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import io
from PIL import Image as Img


class TestViewsCore(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='user')
        self.user_profil = Profil.objects.create(user=self.user)

        with open("tests/unittests/core/testImage.jpg", "rb") as f:
            image_data = f.read()
        self.img = SimpleUploadedFile("Wallpaper.jpg", image_data, content_type="image/jpeg")

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
        response = client.post(reverse("menu", args=(1,)), data={"text": "Test Text"})

        self.assertEqual(response.status_code, 200)
        
        # Get review object from the database
        review = Review.objects.get(pk=1)
        self.assertEqual(review.menu, menu)
        self.assertEqual(review.profil, None)
        self.assertEqual(review.likes, 0)
        self.assertEqual(review.text, "Test Text")
    
    def test_postReview_login(self):
        # Create Menu instance
        menu = Menu.objects.create(name="Test Menu", description="Test")

        client = Client()
        client.login(username="user", password="user")
        response = client.post(reverse("menu", args=(1,)), data={"text": "Test Text"})

        self.assertEqual(response.status_code, 200)
        
        # Get review object from the database
        review = Review.objects.get(pk=1)
        self.assertEqual(review.menu, menu)
        self.assertEqual(review.profil, self.user_profil)
        self.assertEqual(review.likes, 0)
        self.assertEqual(review.text, "Test Text")

    def test_postImage_no_login(self):
        # Create Menu instance
        menu = Menu.objects.create(name="Test Menu", description="Test")
        
        client = Client()

        response = client.post(reverse("menu", args=(1,)), data={"image": self.img})
        
        self.assertEqual(response.status_code, 200)
        
        # Get image object from database
        image = Image.objects.get(pk=1)
        self.assertIsNotNone(image.image)
        self.assertEqual(image.menu, menu)
        self.assertEqual(image.profil, None)
        self.assertEqual(image.likes, 0)
    
    def test_postImage_login(self):
        # Create Menu instance
        menu = Menu.objects.create(name="Test Menu", description="Test")
        
        client = Client()
        client.login(username="user", password="user")

        response = client.post(reverse("menu", args=(1,)), data={"image": self.img})
        
        self.assertEqual(response.status_code, 200)
        
        # Get image object from database
        image = Image.objects.get(pk=1)
        self.assertIsNotNone(image.image)
        self.assertEqual(image.menu, menu)
        self.assertEqual(image.profil, self.user_profil)
        self.assertEqual(image.likes, 0)

    def test_postRating_no_login_valid(self):
        # Create Menu instance
        menu = Menu.objects.create(name="Test Menu", description="Test")
        
        client = Client()
        response = client.post(reverse("menu", args=(1,)), data={"rating": 6})

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
        response = client.post(reverse("menu", args=(1,)), data={"rating": 6})

        self.assertEqual(response.status_code, 200)
        
        # Get review object from the database
        rating = Rating.objects.get(pk=1)
        self.assertEqual(rating.menu, menu)
        self.assertEqual(rating.profil, self.user_profil)
        self.assertEqual(rating.rating, 6)
    
    def test_postRating_no_login_invalid(self):
        # Create Menu instance
        menu = Menu.objects.create(name="Test Menu", description="Test")
        
        client = Client()
        response = client.post(reverse("menu", args=(1,)), data={"rating": 7})

        self.assertEqual(response.status_code, 200)
        
        rating = Rating.objects.filter(pk=1)
        self.assertEqual(len(rating), 0)
        
    def test_postRating_login_change(self):
        # Create Menu instance
        menu = Menu.objects.create(name="Test Menu", description="Test")
        
        client = Client()
        client.login(username="user", password="user")
        response = client.post(reverse("menu", args=(1,)), data={"rating": 6})
        response = client.post(reverse("menu", args=(1,)), data={"rating": 5})

        self.assertEqual(response.status_code, 200)
        
        # Get review object from the database
        rating = Rating.objects.get(pk=1)
        self.assertEqual(rating.menu, menu)
        self.assertEqual(rating.profil, self.user_profil)
        self.assertEqual(rating.rating, 5)
