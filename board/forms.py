from django import forms
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget

from .models import Ad, Reply


class AdForm(forms.ModelForm):
    content = SummernoteTextField()

    class Meta:
        model = Ad
        widgets = {
            'content': SummernoteWidget(),
        }
        fields = [
            'category',
            'title',
            'content',
        ]


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = [
            'content',
        ]
