# Maintained by: Ian, Robin

from django import forms
from .models import Image, Rating, Review, Profil


class ImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'upload-field'}), label="")
    class Meta:
        model = Image
        fields = ['image']
        


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']


class ReviewForm(forms.ModelForm):
    # Resize Textarea from https://stackoverflow.com/questions/2803880/is-there-a-way-to-get-a-textarea-to-stretch-to-fit-its-content-without-using-php
    # 'oninput':'this.style.height = "";this.style.height = this.scrollHeight + "px"'
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'textfield', 'placeholder':'Hier kommentieren...', 'oninput':'this.style.height = "";this.style.height = this.scrollHeight + "px"'}), label='')
    class Meta:
        model = Review
        fields = ['text']


class ProfilPictureForm(forms.ModelForm):
    picture = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'upload-field'}), label="")
    class Meta:
        model = Profil
        fields = ['picture']
 