from .views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('menu/<int:pk>', menu, name="menu"),
    path('allMenu', allMenu, name="allMenu"),
    path('userProfile', userProfile, name="userProfile"),
    path('menuType/<int:pk>', menuType, name="menuType"),
    path('timeline', timeline, name="timeline"),
    path('like/<int:cat>/<int:pk>', like, name="like"),
    path('', index, name="index"),
]

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)