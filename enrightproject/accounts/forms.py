from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

# =======================================================================
# 1. サインアップフォーム (CustomUserCreationForm)
# =======================================================================

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = CustomUser
        
        # UserCreationFormはpassword1/password2を自動で追加
        fields = ('username', 'email') 
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ユーザー名を入力してください'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'メールアドレスを入力してください'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # パスワードフィールドのattrsを更新
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update(
                {
                    'class': 'form-control',
                    'placeholder': 'パスワードを入力してください'
                }
            )
        
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update(
                {
                    'class': 'form-control',
                    'placeholder': 'パスワード（確認用）を再入力してください'
                }
            )


# =======================================================================
# 2. ログインフォーム (CustomUserLoginForm)
# =======================================================================

class CustomUserLoginForm(AuthenticationForm):
    """
    USERNAME_FIELD='email' に対応したカスタムログインフォーム。
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 'username' フィールド（内部では email として機能）のラベルを変更
        if 'username' in self.fields:
            self.fields['username'].label = _('メールアドレス')
            self.fields['username'].widget.attrs['placeholder'] = 'メールアドレス'