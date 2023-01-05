from django import forms
from .models import Image, Rating, Review


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
