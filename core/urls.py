from .views import *
from django.urls import path

urlpatterns = [
    path('app', app, name="app"),
    path('', index, name="index")
]