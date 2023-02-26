from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# The user creation form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    # promoCode = forms.CharField(max_length=10, required=False) ! Unused code
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
