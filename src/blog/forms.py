from django import forms
from django.core.exceptions import ValidationError

from src.blog.models import Category, Post


class CustomAddPostForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    title = forms.CharField(max_length=255)
    slug = forms.SlugField(max_length=255, label='URL', required=True,
                           widget=forms.TextInput(attrs={'class': 'form-input'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'col': 30, 'rows': 10, 'class': 'form-input'}))
    photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-input'}))
    is_published = forms.BooleanField(required=False, initial=True,
                                      widget=forms.CheckboxInput(attrs={'class': 'form-input'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True, empty_label='Not selected',
                                      widget=forms.Select(attrs={'class': 'form-input'}))


class AddPostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Not selected'

    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'col': 30, 'rows': 10, 'class': 'form-input'}),
            'photo': forms.FileInput(attrs={'class': 'form-input'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 100:
            raise ValidationError('Length of title must be less than 200 characters')

        return title


