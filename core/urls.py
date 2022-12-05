from .views import *
from django.urls import path

urlpatterns = [
    path('menu', menu, name="menu"),
    path('allMenu', allMenu, name="allMenu"),
    path('', index, name="index")
]