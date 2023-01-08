from django.db import models
from django.contrib.auth.models import User


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


class Menu(models.Model):
    """
    Menu class for the meals in the Mensa.
    """
    name = models.CharField(max_length=100)  # Name of the meal.
    description = models.TextField()  # Description of the meal.
    date = models.DateField(auto_now_add=True)  # Date of the meal. Default is the current date.
    vegan = models.BooleanField(default=False)  # Is the meal vegan or vegetarian?

    def __str__(self):
        """
        __str__ Returns the name of the meal.

        :return: Returns the name of the meal.
        :rtype: str
        """
        return self.name

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


    

class Review(models.Model):
    """
    Review class for the reviews of the meals.
    """
    profil = models.ForeignKey(Profil, on_delete=models.SET_NULL, null=True)  # Profil of the user who wrote the review. -> If the user doesn't exist anymore, the review is still there.
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)  # Menu of the meal the review is about. -> If the meal doesn't exist anymore, the review is deleted.
    likes = models.IntegerField(default=0)  # Number of likes for the review.
    text = models.TextField()  # Text of the review.
    date = models.DateTimeField(auto_now_add=True)  # Date of the review. Default is the current date.
    
    def __str__(self):
        """
        __str__ Returns the text of the review.

        :return: Returns the text of the review.
        :rtype: str
        """
        return f"{self.profil.user.username}: {self.text[0:20]}..."


class Image(models.Model):
    """
    Image class for the images of the meals.
    """

    profil = models.ForeignKey(Profil, on_delete=models.SET_NULL, null=True)  # Profil of the user who uploaded the image. -> If the user doesn't exist anymore, the image is still there.
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)  # Menu of the meal the image is about. -> If the meal doesn't exist anymore, the image is deleted.
    image = models.ImageField(upload_to='images/')  # Image of the meal.
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
    rating = models.IntegerField(default=0)  # Rating of the meal.
