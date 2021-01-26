from django import forms

from . import models


class CreateForm(forms.ModelForm):
    class Meta:
        model = models.Post
        exclude = ['author']
        fields = ['title', 'description', 'header_image']


class ReportForm(forms.ModelForm):
    class Meta:
        model = models.Report
        exclude = ['author', 'post', 'report_date']
        fields = ['subject', 'sender_email', 'description']
