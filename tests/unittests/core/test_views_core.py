from django.test import TestCase, Client
from django.urls import reverse
from core.models import Menu, Review, Image, Rating, Profil, MenuType
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import io
from PIL import Image as Img
import datetime as dt


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
        menu = Menu.objects.create(name="Test Menu", description="Test", menuType=MenuType.objects.create(name="Test Menu"))

        response = client.get(reverse("menu", args=(menu.pk,)))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "menu.html")

    def test_menu_not_found_get(self):
        client = Client()

        response = client.get(reverse("menu", args=(0,)))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("UTF-8"), "Menu not found")

    def test_allMenu_get(self):
        client = Client()
        response = client.get(reverse("allMenu"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "allMenu.html")

    def test_postReview_no_login(self):
        # Create Menu instance
        menu = Menu.objects.create(name="Test Menu", description="Test", menuType=MenuType.objects.create(name="Test Menu"))

        client = Client()
        response = client.post(reverse("menu", args=(1,)), data={"text": "Test Text"})

        self.assertEqual(response.status_code, 200)
        
        # Get review object from the database
        review = Review.objects.filter(pk=1)
        self.assertEqual(len(review), 1)
        review = review[0]
        self.assertEqual(review.menu, menu)
        self.assertEqual(review.profil, None)
        self.assertEqual(review.likes, 0)
        self.assertEqual(review.text, "Test Text")
    
    def test_postReview_login(self):
        # Create Menu instance
        menu = Menu.objects.create(name="Test Menu", description="Test", menuType=MenuType.objects.create(name="Test Menu"))

        client = Client()
        client.login(username="user", password="user")
        response = client.post(reverse("menu", args=(1,)), data={"text": "Test Text"})

        self.assertEqual(response.status_code, 200)
        
        # Get review object from the database
        review = Review.objects.filter(pk=1)
        self.assertEqual(len(review), 1)
        review = review[0]
        self.assertEqual(review.menu, menu)
        self.assertEqual(review.profil, self.user_profil)
        self.assertEqual(review.likes, 0)
        self.assertEqual(review.text, "Test Text")

    def test_postImage_no_login(self):
        # Create Menu instance
        menu = Menu.objects.create(name="Test Menu", description="Test", menuType=MenuType.objects.create(name="Test Menu"))
        
        client = Client()

        response = client.post(reverse("menu", args=(1,)), data={"image": self.img})
        
        self.assertEqual(response.status_code, 200)
        
        # Get image object from database
        image = Image.objects.filter(pk=1)
        self.assertEqual(len(image), 1)
        image = image[0]
        self.assertIsNotNone(image.image)
        self.assertEqual(image.menu, menu)
        self.assertEqual(image.profil, None)
        self.assertEqual(image.likes, 0)
    
    def test_postImage_login(self):
        # Create Menu instance
        menu = Menu.objects.create(name="Test Menu", description="Test", menuType=MenuType.objects.create(name="Test Menu"))
        
        client = Client()
        client.login(username="user", password="user")

        response = client.post(reverse("menu", args=(1,)), data={"image": self.img})
        
        self.assertEqual(response.status_code, 200)
        
        # Get image object from database
        image = Image.objects.filter(pk=1)
        self.assertEqual(len(image), 1)
        image = image[0]
        self.assertIsNotNone(image.image)
        self.assertEqual(image.menu, menu)
        self.assertEqual(image.profil, self.user_profil)
        self.assertEqual(image.likes, 0)

    def test_postRating_no_login_valid(self):
        # Create Menu instance
        menu = Menu.objects.create(name="Test Menu", description="Test", menuType=MenuType.objects.create(name="Test Menu"))
        
        client = Client()
        response = client.post(reverse("menu", args=(1,)), data={"rating": 5})

        self.assertEqual(response.status_code, 200)
        
        # Get review object from the database
        rating = Rating.objects.filter(pk=1)
        self.assertEqual(len(rating), 1)
        rating = rating[0]
        self.assertEqual(rating.menu, menu)
        self.assertEqual(rating.profil, None)
        self.assertEqual(rating.rating, 5)
    
    def test_postRating_login_valid(self):
        # Create Menu instance
        menu = Menu.objects.create(name="Test Menu", description="Test", menuType=MenuType.objects.create(name="Test Menu"))
        
        client = Client()
        client.login(username="user", password="user")
        response = client.post(reverse("menu", args=(1,)), data={"rating": 5})

        self.assertEqual(response.status_code, 200)
        
        # Get review object from the database
        rating = Rating.objects.filter(pk=1)
        self.assertEqual(len(rating), 1)
        rating = rating[0]
        self.assertEqual(rating.menu, menu)
        self.assertEqual(rating.profil, self.user_profil)
        self.assertEqual(rating.rating, 5)
    
    def test_postRating_no_login_invalid(self):
        # Create Menu instance
        menu = Menu.objects.create(name="Test Menu", description="Test", menuType=MenuType.objects.create(name="Test Menu"))
        
        client = Client()
        response = client.post(reverse("menu", args=(1,)), data={"rating": 7})

        self.assertEqual(response.status_code, 200)
        
        rating = Rating.objects.filter(pk=1)
        self.assertEqual(len(rating), 0)
        
    def test_postRating_login_change(self):
        # Create Menu instance
        menu = Menu.objects.create(name="Test Menu", description="Test", menuType=MenuType.objects.create(name="Test Menu"))
        
        client = Client()
        client.login(username="user", password="user")
        response = client.post(reverse("menu", args=(1,)), data={"rating": 4})
        response = client.post(reverse("menu", args=(1,)), data={"rating": 5})

        self.assertEqual(response.status_code, 200)
        
        # Get review object from the database
        rating = Rating.objects.filter(pk=1)
        self.assertEqual(len(rating), 1)
        rating = rating[0]
        self.assertEqual(rating.menu, menu)
        self.assertEqual(rating.profil, self.user_profil)
        self.assertEqual(rating.rating, 5)
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
        
        menu = Menu.objects.create(name="Test Menu", description="Test", menuType=MenuType.objects.create(name="Test Menu", date=dt.date(2018, 1, 1)))
        
        response = client.get(reverse("menuType", args=(menu.menuType.pk,)))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "menuType.html")
    
    def test_menuType_not_found_get(self):
        client = Client()
        
        response = client.get(reverse("menuType", args=(0,)))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("UTF-8"), "Menutype not found")
    
    def test_timeline_get(self):
        client = Client()
        
        response = client.get(reverse("timeline"))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "timeline.html")
    
    def test_like_like_get(self):
        menu = Menu.objects.create(name="Test Menu", description="Test", menuType=MenuType.objects.create(name="Test Menu"))
        review = Review.objects.create(menu=menu, likes=0, text="Test")
        
        client = Client()
        
        response = client.get(reverse("like", args=(1, 1)))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("UTF-8"), "1")
        review.refresh_from_db()
        self.assertEqual(review.likes, 1)
        
    def test_like_dislike_below_get(self):
        menu = Menu.objects.create(name="Test Menu", description="Test", menuType=MenuType.objects.create(name="Test Menu"))
        review = Review.objects.create(menu=menu, likes=0, text="Test")
        
        client = Client()
        
        response = client.get(reverse("like", args=(1, 1)), data={"dislike": "YES"})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("UTF-8"), "0")
        review.refresh_from_db()
        self.assertEqual(review.likes, 0)
    
    def test_like_dislike_get(self):
        menu = Menu.objects.create(name="Test Menu", description="Test", menuType=MenuType.objects.create(name="Test Menu"))
        review = Review.objects.create(menu=menu, likes=1, text="Test")
        
        client = Client()
        
        response = client.get(reverse("like", args=(1, 1)), data={"dislike": "YES"})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("UTF-8"), "0")
        review.refresh_from_db()
        self.assertEqual(review.likes, 0)
    
    def test_like_cat_not_get(self):
        client = Client()
        
        response = client.get(reverse("like", args=(3, 1)))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("UTF-8"), "Category not found")
    
    def test_like_cat_not_found(self):
        client = Client()
        
        response = client.get(reverse("like", args=(1, 1)))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("UTF-8"), "Post not found")
    
    def test_leaderboard_get_no_login(self):
        client = Client()
        
        response = client.get(reverse("leaderboard"))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "leaderboard.html")
    
    def test_leaderboard_get_login(self):
        client = Client()
        client.login(username="user", password="user")
        
        response = client.get(reverse("leaderboard"))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "leaderboard.html")
