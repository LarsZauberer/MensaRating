from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

import datetime as dt

from gdstorage.storage import GoogleDriveStorage
from django.core.files.storage import FileSystemStorage

if settings.HEROKU:
    # Define Google Drive Storage
    storage_service = GoogleDriveStorage()
else:
    # Define normal MEDIA Storage Directory
    storage_service = FileSystemStorage()
    


class Profil(models.Model):
    """
    Profil class for the user. A custom class to add more information to the user.
    """
    karma = models.IntegerField(default=0)  # Karma points for the posts from the user. 
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # User linked to the profil. -> The profil is deleted when the user is deleted.

    def __str__(self):
        """
        __str__ Returns the username of the user owning the profil.

        :return: Returns the username of the user owning the profil.
        :rtype: str
        """
        return self.user.username


class MenuType(models.Model):
    """
    MenuType class for the type of the menu
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        """
        __str__ Returns the name of the mealtype.

        :return: Returns the name of the mealtype.
        :rtype: str
        """
        return self.name


class Menu(models.Model):
    """
    Menu class for the meals in the Mensa.
    """
    name = models.CharField(max_length=100)  # Name of the meal.
    description = models.TextField()  # Description of the meal.
    date = models.DateField(default=dt.date.today())  # Date of the meal. Default is the current date.
    vegetarian = models.BooleanField(default=False)  # Is the meal vegetarian?
    vegan = models.BooleanField(default=False)  # Is the meal vegan
    menuType = models.ForeignKey(MenuType, on_delete=models.CASCADE)

    def __str__(self):
        """
        __str__ Returns the name of the meal.

        :return: Returns the name of the meal.
        :rtype: str
        """
        return self.name
    
    def setMenuType(self):
        """
        getMenuType Get the corresponding menuType of the menu

        :return: The corresponding menuType of the menu
        :rtype: MenuType
        """
        if not MenuType.objects.filter(name=self.name).exists():
            MenuType.objects.create(name=self.name)

        return MenuType.objects.get(name=self.name)


class Review(models.Model):
    """
    Review class for the reviews of the meals.
    """
    profil = models.ForeignKey(Profil, on_delete=models.SET_NULL, null=True)  # Profil of the user who wrote the review. -> If the user doesn't exist anymore, the review is still there.
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)  # Menu of the meal the review is about. -> If the meal doesn't exist anymore, the review is deleted.
    likes = models.IntegerField(default=0)  # Number of likes for the review.
    text = models.TextField(max_length=200) # Text of the review.


    date = models.DateTimeField(auto_now_add=True)  # Date of the review. Default is the current date.
    
    def __str__(self):
        """
        __str__ Returns the text of the review.

        :return: Returns the text of the review.
        :rtype: str
        """
        #return f"{self.profil.user.username}: {self.text[0:20]}..."
        return f"rew.{self.pk}"


class Image(models.Model):
    """
    Image class for the images of the meals.
    """

    profil = models.ForeignKey(Profil, on_delete=models.SET_NULL, null=True)  # Profil of the user who uploaded the image. -> If the user doesn't exist anymore, the image is still there.
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)  # Menu of the meal the image is about. -> If the meal doesn't exist anymore, the image is deleted.
    image = models.ImageField(upload_to='images/', storage=storage_service)  # Image of the meal.
    likes = models.IntegerField(default=0)  # Number of likes for the image.
    date = models.DateTimeField(auto_now_add=True)  # Date of the image. Default is the current date.
    
    def __str__(self):
        """
        __str__ Returns the name of the image.

        :return: Returns the name of the image.
        :rtype: str
        """
        return f"{self.profil.user.username}: {self.image.name}"


class Rating(models.Model):
    profil = models.ForeignKey(Profil, on_delete=models.SET_NULL, null=True)  # Profil of the user who rated the meal. -> If the user doesn't exist anymore, the rating is still there.
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)  # Menu of the meal the rating is about. -> If the meal doesn't exist anymore, the rating is deleted.
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)  # Rating of the meal.


class Badge(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to="images/", storage=storage_service)

    condition_category = models.IntegerField()
    count = models.IntegerField()
    
    def __str__(self):
        return self.name
