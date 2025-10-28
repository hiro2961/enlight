from django.forms import ModelForm
from .models import PhotoPost
from django import forms

class PhotoPostForm(ModelForm):
    
    class Meta:
        
        model = PhotoPost
        fields = ['category', 'title', 'comment', 'image1', 'image2']

        widgets = {
            'category': forms.Select(attrs={'class': 'form-style'}), 
            'title': forms.TextInput(attrs={'class': 'form-style', 'placeholder': '投稿タイトルを入力してください'}), 
            'comment': forms.Textarea(attrs={'class': 'form-style', 'rows': 5, 'placeholder': '内容を入力してください'}), 
            'image1': forms.ClearableFileInput(attrs={'class': 'form-control-file'}), 
            'image2': forms.ClearableFileInput(attrs={'class': 'form-control-file'}), 
        }

class SearchForm(forms.Form):
    keyword = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'タイトルまたはキーワードで検索',
            'class': 'search-input',
            'autocomplete': 'off',
        })
    )
