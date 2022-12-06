from .views import *
from django.urls import path

urlpatterns = [
    path('menu/<int:pk>', menu, name="menu"),
    path('allMenu', allMenu, name="allMenu"),
    path('postReview/<int:pk>', postReview, name="postReview"),
    path('postImage/<int:pk>', postImage, name="postImage"),
    path('postRating<int:pk>', postRating, name="postRating"),
    path('', index, name="index")
]