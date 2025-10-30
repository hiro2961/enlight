from django.forms import ModelForm
from .models import PhotoPost
from django import forms

class PhotoPostForm(ModelForm):
    
    class Meta:
        
        model = PhotoPost
        # ★★★ 修正箇所: 'category'をfieldsから削除 ★★★
        fields = ['title', 'comment', 'image1', 'image2']

        widgets = {
            # ★★★ 修正箇所: 'category'に関する記述を削除 ★★★
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