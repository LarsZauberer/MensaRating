from django.test import TestCase, Client
from django.urls import reverse

class TestViewsUsers(TestCase):
    def setUp(self):
        pass
    
    def test_users_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_users_register(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_users_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'logout.html')

    def test_users_password_reset(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset.html')

    def test_users_password_reset_done(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset_done.html')

    def test_users_password_reset_confirm(self):
        response = self.client.get(reverse('password_reset_confirm', args=[123, "123"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset_confirm.html')

    def test_users_password_reset_confirm(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset_complete.html')