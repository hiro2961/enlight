# =======================================================================
# 修正後の accounts/urls.py の完全版
# =======================================================================
from django.urls import path
# from django.contrib.auth import views as auth_views # <-- カスタムビューを使うため不要
from django.contrib.auth.views import LogoutView # LogoutViewのみ必要
from . import views # accounts/views.py 全体をインポート

# URLパターンを逆引きできるように名前を付ける
app_name = 'accounts'

# URLパターンを登録する変数
urlpatterns = [
    # ------------------------------------------------------------------
    # 【一般の方 (citizen)】
    # ------------------------------------------------------------------
    # サインアップ
    path('citizen/signup/',
          views.CitizenSignUpView.as_view(), 
          name='citizen_signup'),

    # サインアップ完了
    path('citizen/signup_success/',
          views.CitizenSignUpSuccessView.as_view(),
          name='citizen_signup_success'),

    # ★★★ 修正箇所: カスタムログインビューを参照 ★★★
    path('citizen/login/',
          views.CitizenLoginView.as_view(), # カスタムビュー (権限チェック付き)
          name='citizen_login'),

    # ログアウト (Django標準LogoutViewを使用)
    path('citizen/logout/',
          LogoutView.as_view(template_name='citizen/logout.html'),
          name='citizen_logout'),


    # ------------------------------------------------------------------
    # 【要支援者 (rescue)】
    # ------------------------------------------------------------------
    # サインアップ
    path('rescue/signup/',
          views.RescueSignUpView.as_view(),
          name='rescue_signup'),

    # サインアップ完了
    path('rescue/signup_success/',
          views.RescueSignUpSuccessView.as_view(),
          name='rescue_signup_success'),
    
    # ★★★ 修正箇所: カスタムログインビューを参照 ★★★
    path('rescue/login/',
          views.RescueLoginView.as_view(), # カスタムビュー (権限チェック付き)
          name='rescue_login'),

    # ログアウト (Django標準LogoutViewを使用)
    path('rescue/logout/',
          LogoutView.as_view(template_name='rescue/logout.html'),
          name='rescue_logout'),


    # ------------------------------------------------------------------
    # 【支援者 (supporter)】
    # ------------------------------------------------------------------
    # サインアップ (views.pyで定義されているものを使用)
    path('supporter/signup/',
          views.SupporterSignUpView.as_view(),
          name='supporter_signup'),
          
    # サインアップ完了 (views.pyで定義されているものを使用)
    path('supporter/signup_success/',
          views.SupporterSignUpSuccessView.as_view(),
          name='supporter_signup_success'),
    
    # ★★★ 修正箇所: カスタムログインビューを参照 ★★★
    path('supporter/login/',
          views.SupporterLoginView.as_view(), # カスタムビュー (権限チェック付き)
          name='supporter_login'),

    # ログアウト (Django標準LogoutViewを使用)
    path('supporter/logout/',
          LogoutView.as_view(template_name='supporter/logout.html'),
          name='supporter_logout'),

]