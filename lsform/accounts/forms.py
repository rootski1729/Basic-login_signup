from django import forms
from .models import Blogpost

class Blogpostform(forms.ModelForm):
    class Meta:
        model = Blogpost
        fields = ['title', 'image', 'category', 'summary', 'content', 'status']
        