from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import register
from django.contrib.auth import views as auth_views


class TestUrlsUsers(SimpleTestCase):
    def test_register_url(self):
        url = reverse("register")
        self.assertEqual(resolve(url).func, register)

    def test_login_url(self):
        url = reverse("login")
        self.assertEqual(resolve(url).route, "users/login")

    def test_logout_url(self):
        url = reverse("logout")
        self.assertEqual(resolve(url).route, "users/logout")

    def test_password_reset_url(self):
        url = reverse("password_reset")
        self.assertEqual(resolve(url).route, "users/password-reset")

    def test_password_reset_done_url(self):
        url = reverse("password_reset_done")
        self.assertEqual(resolve(url).route, "users/password-reset/done")
    
    def test_password_reset_confirm_url(self):
        url = reverse("password_reset_confirm", args=[1234, "1234"])
        self.assertEqual(resolve(url).route, "users/password-reset-confirm<uidb64>/<token>/")
    
    def test_password_reset_done_url(self):
        url = reverse("password_reset_complete")
        self.assertEqual(resolve(url).route, "users/password-reset-complete")
    