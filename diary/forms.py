from django import forms
from django.core.exceptions import ValidationError
from django.forms import BooleanField

from diary.models import Entry


class StyleFormMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class EntryForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Entry
        exclude = ['view_counter', 'created_at', 'author']
        # fields = ('title', 'content', 'image', 'author',)
