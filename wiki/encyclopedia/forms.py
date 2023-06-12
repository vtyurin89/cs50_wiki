from django import forms
from django.core.exceptions import ValidationError

from . import util


def validate_entry(title):
    check_entry = util.get_entry(title)
    if check_entry:
        raise ValidationError(
            (f"Entry with the name '{title}' already exists!"),
            params={"title": title},
        )


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", validators=[validate_entry], widget=forms.TextInput(attrs={'name': 'title'}))
    content = forms.CharField(label="Markdown content", widget=forms.Textarea(attrs={'name': 'content', 'class': 'new-entry-textarea'}))


class EditEntryForm(forms.Form):
    content = forms.CharField(label="Markdown content", widget=forms.Textarea(attrs={'name': 'content', 'class': 'new-entry-textarea'}))
