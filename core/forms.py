from django import forms
from .models import Image, Rating, Review


class ImageForm(forms.ModelForm):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'upload-field'}), label="")
    class Meta:
        model = Image
        fields = ['image']
        


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']


class ReviewForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'textfield'}), label='')
    class Meta:
        model = Review
        fields = ['text']

       


 