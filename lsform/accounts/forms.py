from django import forms
from .models import Blogpost

class Blogpostform(forms.ModelForm):
    class Meta:
        model = Blogpost
        fields = ['title', 'content','summary' ,'image', 'category', 'status']  # Include 'status' field

    def __init__(self, *args, **kwargs):
        super(Blogpostform, self).__init__(*args, **kwargs)
        self.fields['status'].widget = forms.RadioSelect(choices=[
            ('published', 'Published'),
            ('drafted', 'Drafted')
        ])
        self.fields['status'].initial = 'published'
        