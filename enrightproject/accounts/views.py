from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView # ★追加：ログインビュー用★
# from .forms import CustomAuthenticationForm # 独自のログインフォームを使う場合はインポート

# =======================================================================
# 1. 市民 (CITIZEN)
# =======================================================================

class CitizenSignUpView(CreateView):
    '''市民用サインアップページのビュー'''
    form_class = CustomUserCreationForm
    template_name = "citizen/signup.html"
    success_url = reverse_lazy('accounts:citizen_signup_success')

    def form_valid(self, form):
        user = form.save()
        self.object = user
        return super().form_valid(form)

class CitizenSignUpSuccessView(TemplateView):
    '''市民用サインアップ完了ページのビュー'''
    template_name = 'citizen/signup_success.html'

class CitizenLoginView(LoginView):
    '''市民用ログインページのビュー'''
    # forms.pyで独自のフォーム(例:CustomAuthenticationForm)を定義している場合は、form_classを指定
    # form_class = CustomAuthenticationForm
    template_name = 'citizen/login.html' # ★修正：テンプレートパス★
    
    def get_success_url(self):
        # ログイン後の市民向けリダイレクト先を定義
        return reverse_lazy('main:index') # 例として 'main:index' にリダイレクト

# =======================================================================
# 2. 救助隊 (RESCUE)
# =======================================================================

class RescueSignUpView(CreateView):
    '''救助隊用サインアップページのビュー'''
    form_class = CustomUserCreationForm
    template_name = "rescue/signup.html"
    success_url = reverse_lazy('accounts:rescue_signup_success')

    def form_valid(self, form):
        user = form.save()
        self.object = user
        return super().form_valid(form)

class RescueSignUpSuccessView(TemplateView):
    '''救助隊用サインアップ完了ページのビュー'''
    template_name = 'rescue/signup_success.html'
    
class RescueLoginView(LoginView):
    '''救助隊用ログインページのビュー'''
    # form_class = CustomAuthenticationForm
    template_name = 'rescue/login.html' # ★修正：テンプレートパス★
    
    def get_success_url(self):
        # ログイン後の救助隊向けリダイレクト先を定義
        return reverse_lazy('main:index') # 例として 'main:index' にリダイレクト

# =======================================================================
# 3. サポーター (SUPPORTER)
# =======================================================================

class SupporterSignUpView(CreateView):
    '''サポーター用サインアップページのビュー'''
    form_class = CustomUserCreationForm
    template_name = "supporter/signup.html"
    success_url = reverse_lazy('accounts:supporter_signup_success')

    def form_valid(self, form):
        user = form.save()
        self.object = user
        return super().form_valid(form)

class SupporterSignUpSuccessView(TemplateView):
    '''サポーター用サインアップ完了ページのビュー'''
    template_name = 'supporter/signup_success.html'
    
class SupporterLoginView(LoginView):
    '''サポーター用ログインページのビュー'''
    # form_class = CustomAuthenticationForm
    template_name = 'supporter/login.html' # ★修正：テンプレートパス★
    
    def get_success_url(self):
        # ログイン後のサポーター向けリダイレクト先を定義
        return reverse_lazy('main:index') # 例として 'main:index' にリダイレクト

# =======================================================================