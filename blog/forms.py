from django import forms

from . import models


class CreateForm(forms.ModelForm):
    class Meta:
        model = models.Blog
        exclude = ['author']
        fields = ['title', 'description', 'header_image']
