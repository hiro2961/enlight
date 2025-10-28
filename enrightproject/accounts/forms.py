from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = CustomUser
        
        fields = ('username', 'email') 

        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ユーザー名を入力してください'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'メールアドレスを入力してください'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'パスワードを入力してください'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'パスワード（確認用）を再入力してください'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'password1' in self.fields:
            self.fields['password1'].widget = forms.PasswordInput(
                attrs={
                    'class': 'form-control'                    
                }
            )
        
        if 'password2' in self.fields:
            self.fields['password2'].widget = forms.PasswordInput(
                attrs={
                    'class': 'form-control'
                }
            )
from django import forms
from django.contrib.auth.forms import UserCreationForm
# CustomUserモデルをインポート
from .models import CustomUser 
# ログインフォームをカスタマイズする場合は、AuthenticationFormもインポート

class CustomUserCreationForm(UserCreationForm):
    '''
    カスタムユーザーモデル (CustomUser) に対応したサインアップフォーム。
    UserCreationFormを継承することで、パスワードのハッシュ化や二重入力チェックは
    Djangoの標準機能が自動的に行ってくれます。
    '''
    
    class Meta:
        model = CustomUser
        
        # ★★★修正点: 'password1' と 'password2' をfieldsに含める★★★
        # これにより、ユーザー登録時にパスワードが正しく入力・保存されます。
        fields = ('username', 'email', 'password1', 'password2') 
        
        # widgetsの設定
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ユーザー名を入力してください'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'メールアドレスを入力してください'}),
            # UserCreationFormで使われるpassword1/password2のカスタム
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'パスワードを入力してください'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'パスワード（確認用）を再入力してください'}),
        }

    # __init__ メソッドは、widgetsでattrsを設定しているため、
    # このように再度上書きする処理は冗長ですが、前回いただいたコードに合わせて残します。
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update(
                {
                    'class': 'form-control',
                    'placeholder': 'パスワードを入力してください' # プレースホルダーを明示的に追加
                }
            )
        
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update(
                {
                    'class': 'form-control',
                    'placeholder': 'パスワード（確認用）を再入力してください' # プレースホルダーを明示的に追加
                }
            )

# ----------------------------------------------------------------------
# 補足: CustomAuthenticationForm (標準のLoginViewを使う場合は通常不要)
# ----------------------------------------------------------------------

# 独自の認証フォームを作成する場合は、この下に記述します。
# from django.contrib.auth.forms import AuthenticationForm
# 
# class CustomAuthenticationForm(AuthenticationForm):
#     class Meta:
#         model = CustomUser # 認証フォームでは通常モデルは指定しません
#         fields = ('username', 'password')
#     
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs['class'] = 'form-control'
#         self.fields['password'].widget.attrs['class'] = 'form-control'e