
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView # TemplateViewが必要
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.forms import ValidationError
from django.contrib.auth.models import Group # グループモデルのインポート


def add_user_to_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
    except Group.DoesNotExist:
        print(f"Warning: Group '{group_name}' does not exist.")


# =======================================================================
# 1. 一般市民 (CITIZEN)
# =======================================================================

class CitizenSignUpView(CreateView):
    '''市民用サインアップページのビュー'''
    form_class = CustomUserCreationForm
    template_name = "citizen/signup.html"
    success_url = reverse_lazy('accounts:citizen_signup_success')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = False # 一般市民は is_staff=False
        user.save()
        add_user_to_group(user, '一般市民')
        self.object = user
        return super().form_valid(form)

# ★★★  ★★★
class CitizenSignUpSuccessView(TemplateView):
    '''市民用サインアップ完了ページのビュー'''
    template_name = 'citizen/signup_success.html'
# ★★★ ここまで追加 ★★★

class CitizenLoginView(LoginView):
    '''市民用ログインページのビュー（ログイン制限あり）'''
    template_name = 'citizen/login.html'
    
    def get_success_url(self):
        return reverse_lazy('main:index')

    def form_valid(self, form):
        user = form.get_user()
        if user.is_staff or not user.groups.filter(name='一般市民').exists():
            form.add_error(
                None, 
                ValidationError('このログインフォームは一般市民専用です。アカウントの種類を確認してください。')
            )
            return self.form_invalid(form)
        return super().form_valid(form)


# =======================================================================
# 2. 要支援者 (RESCUE)
# =======================================================================

class RescueSignUpView(CreateView):
    '''要支援者用サインアップページのビュー'''
    form_class = CustomUserCreationForm
    template_name = "rescue/signup.html"
    success_url = reverse_lazy('accounts:rescue_signup_success')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = False # 要支援者は is_staff=False
        user.save()
        add_user_to_group(user, '要支援者')
        self.object = user
        return super().form_valid(form)
    
# ★★★ 不足していたビューを追加 ★★★
class RescueSignUpSuccessView(TemplateView):
    '''要支援者用サインアップ完了ページのビュー'''
    template_name = 'rescue/signup_success.html'
# ★★★ ここまで追加 ★★★

class RescueLoginView(LoginView):
    '''要支援者用ログインページのビュー（ログイン制限あり）'''
    template_name = 'rescue/login.html'
    
    def get_success_url(self):
        return reverse_lazy('main:index')

    def form_valid(self, form):
        user = form.get_user()
        if user.is_staff or not user.groups.filter(name='要支援者').exists():
            form.add_error(
                None, 
                ValidationError('このログインフォームは要支援者専用です。アカウントの種類を確認してください。')
            )
            return self.form_invalid(form)
        return super().form_valid(form)
    
# =======================================================================
# 3. 支援者 (SUPPORTER)
# =======================================================================

class SupporterSignUpView(CreateView):
    '''サポーター用サインアップページのビュー'''
    form_class = CustomUserCreationForm
    template_name = "supporter/signup.html"
    success_url = reverse_lazy('accounts:supporter_signup_success')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = True # 支援者は is_staff=True
        user.save()
        # グループ追加は is_staff で識別するため省略
        self.object = user
        return super().form_valid(form)
    
# ★★★ 不足していたビューを追加 ★★★
class SupporterSignUpSuccessView(TemplateView):
    '''サポーター用サインアップ完了ページのビュー'''
    template_name = 'supporter/signup_success.html'
# ★★★ ここまで追加 ★★★

class SupporterLoginView(LoginView):
    '''サポーター用ログインページのビュー（ログイン制限あり）'''
    template_name = 'supporter/login.html'
    
    def get_success_url(self):
        return reverse_lazy('main:index')

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_staff:
            form.add_error(
                None, 
                ValidationError('このログインフォームは支援者専用です。アカウントの種類を確認してください。')
            )
            return self.form_invalid(form)
        return super().form_valid(form)