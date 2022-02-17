from django import forms
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.widgets import CKEditorWidget

from .models import *

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].disabled = True
        self.fields['date'].disabled = True

    class Meta:
        model = Post
        fields = '__all__'


class ResponseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].disabled = True
        self.fields['date'].disabled = True
        self.fields['post'].disabled = True

    class Meta:
        model = Response
        fields = '__all__'