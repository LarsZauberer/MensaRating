from .views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('menu/<int:pk>', menu, name="menu"),
    path('allMenu', allMenu, name="allMenu"),
    path('postReview/<int:pk>', postReview, name="postReview"),
    path('postImage/<int:pk>', postImage, name="postImage"),
    path('postRating<int:pk>', postRating, name="postRating"),
    path('userProfile', userProfile, name="userProfile"),
    path('', index, name="index")
]

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)