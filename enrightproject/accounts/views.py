from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from .forms import CustomUserCreationForm, CustomUserLoginForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.forms import ValidationError
from django.contrib.auth.models import Group # 互換性のためインポートを維持

# 注意: この関数はグループが存在しない場合、ユーザーをグループに追加しません。
# ログイン認証には使用されなくなりましたが、サインアップロジックには残っています。
def add_user_to_group(user, group_name):
    '''ユーザーを指定されたグループに追加するヘルパー関数'''
    try:
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
    except Group.DoesNotExist:
        print(f"Warning: Group '{group_name}' does not exist.")


# =======================================================================
# 1. 一般市民 (CITIZEN) - user_type=1
# =======================================================================

class CitizenSignUpView(CreateView):
    '''市民用サインアップページのビュー'''
    form_class = CustomUserCreationForm
    template_name = "citizen/signup.html"
    success_url = reverse_lazy('accounts:citizen_signup_success')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.user_type = 1 # 1: 一般ユーザー
        user.save() 
        add_user_to_group(user, '一般市民') 
        self.object = user
        return super(CreateView, self).form_valid(form)


class CitizenSignUpSuccessView(TemplateView):
    '''市民用サインアップ完了ページのビュー'''
    template_name = 'citizen/signup_success.html'


class CitizenLoginView(LoginView):
    '''市民用ログインページのビュー（ログイン制限あり）'''
    template_name = 'citizen/login.html'
    form_class = CustomUserLoginForm
    
    def get_success_url(self):
        return reverse_lazy('main:index')

    def form_valid(self, form):
        user = form.get_user()
        
        # 修正箇所: ログインユーザーが管理者 (is_staff) またはユーザー種別が '一般ユーザー' (1) ではない場合、エラーとする
        if user.is_staff or user.user_type != 1:
            form.add_error(
                None, 
                ValidationError('このログインフォームは一般市民専用です。アカウントの種類を確認してください。')
            )
            return self.form_invalid(form)
        return super().form_valid(form)


# =======================================================================
# 2. 要支援者 (RESCUE) - user_type=2
# =======================================================================

class RescueSignUpView(CreateView):
    '''要支援者用サインアップページのビュー'''
    form_class = CustomUserCreationForm
    template_name = "rescue/signup.html"
    success_url = reverse_lazy('accounts:rescue_signup_success')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.user_type = 2 # 2: 要支援者
        user.save() 
        add_user_to_group(user, '要支援者')
        self.object = user
        return super(CreateView, self).form_valid(form)
    
    
class RescueSignUpSuccessView(TemplateView):
    '''要支援者用サインアップ完了ページのビュー'''
    template_name = 'rescue/signup_success.html'


class RescueLoginView(LoginView):
    '''要支援者用ログインページのビュー（ログイン制限あり）'''
    template_name = 'rescue/login.html'
    form_class = CustomUserLoginForm
    
    def get_success_url(self):
        return reverse_lazy('main:index')

    def form_valid(self, form):
        user = form.get_user()
        
        # 修正箇所: ログインユーザーが管理者 (is_staff) またはユーザー種別が '要支援者' (2) ではない場合、エラーとする
        if user.is_staff or user.user_type != 2:
            form.add_error(
                None, 
                ValidationError('このログインフォームは要支援者専用です。アカウントの種類を確認してください。')
            )
            return self.form_invalid(form)
        return super().form_valid(form)


# =======================================================================
# 3. 支援者 (SUPPORTER) - user_type=3
# =======================================================================

class SupporterSignUpView(CreateView):
    '''サポーター用サインアップページのビュー'''
    form_class = CustomUserCreationForm
    template_name = "supporter/signup.html"
    success_url = reverse_lazy('accounts:supporter_signup_success')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.user_type = 3 # 3: 支援者
        user.save() 
        add_user_to_group(user, '支援者')
        self.object = user
        return super(CreateView, self).form_valid(form)
    
    
class SupporterSignUpSuccessView(TemplateView):
    '''サポーター用サインアップ完了ページのビュー'''
    template_name = 'supporter/signup_success.html'


class SupporterLoginView(LoginView):
    '''サポーター用ログインページのビュー（ログイン制限あり）'''
    template_name = 'supporter/login.html'
    form_class = CustomUserLoginForm
    
    def get_success_url(self):
        return reverse_lazy('main:index') 
        
    def form_valid(self, form):
        user = form.get_user()
        
        # 修正箇所: ログインユーザーが管理者 (is_staff) またはユーザー種別が '支援者' (3) ではない場合、エラーとする
        if user.is_staff or user.user_type != 3:
            form.add_error(
                None, 
                ValidationError('このログインフォームは支援者専用です。アカウントの種類を確認してください。')
            )
            return self.form_invalid(form)
        return super().form_valid(form)


# =======================================================================
# 4. 管理者 (ADMIN)
# =======================================================================