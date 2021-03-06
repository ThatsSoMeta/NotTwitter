from django import forms
from .models import Tweet


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = [
            'text'
        ]
        labels = {
            'text': 'Tweet'
        }
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'autofocus': 'on',
                    'class': 'reply-text',
                    'placeholder': "What's on your mind?"
                }
            )
        }
