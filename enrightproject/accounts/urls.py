from django.urls import path
from django.contrib.auth import views as auth_views
from . import views # accounts/views.py 全体をインポート

# URLパターンを逆引きできるように名前を付ける
app_name = 'accounts'

# URLパターンを登録する変数
urlpatterns = [
    # ------------------------------------------------------------------
    # 【一般の方 (citizen)】 - pathの呼び出しを views.ClassName.as_view() に変更
    # ------------------------------------------------------------------
    # サインアップ
    path('citizen/signup/',
         views.CitizenSignUpView.as_view(), # ★修正: views. を使い、ビュークラス名を明示
         name='citizen_signup'),

    # サインアップ完了
    path('citizen/signup_success/',
         views.CitizenSignUpSuccessView.as_view(), # ★修正: views. を使い、ビュークラス名を明示
         name='citizen_signup_success'),

    # ログイン (auth_viewsなので変更なし)
    path('citizen/login/',
         auth_views.LoginView.as_view(template_name='citizen/login.html'),
         name='citizen_login'),

    # ログアウト (auth_viewsなので変更なし)
    path('citizen/logout/',
         auth_views.LogoutView.as_view(template_name='citizen/logout.html'),
         name='citizen_logout'),


    # ------------------------------------------------------------------
    # 【要支援者 (rescue)】 - pathの呼び出しを views.ClassName.as_view() に変更
    # ------------------------------------------------------------------
    # サインアップ
    path('rescue/signup/',
         views.RescueSignUpView.as_view(), # ★修正: views. を使い、ビュークラス名を明示
         name='rescue_signup'),

    # サインアップ完了
    path('rescue/signup_success/',
         views.RescueSignUpSuccessView.as_view(), # ★修正: views. を使い、ビュークラス名を明示
         name='rescue_signup_success'),
    
    # ログイン (auth_viewsなので変更なし)
    path('rescue/login/',
         auth_views.LoginView.as_view(template_name='rescue/login.html'),
         name='rescue_login'),

    # ログアウト (auth_viewsなので変更なし)
    path('rescue/logout/',
         auth_views.LogoutView.as_view(template_name='rescue/logout.html'),
         name='rescue_logout'),


    # ------------------------------------------------------------------
    # 【支援者 (supporter)】 - pathの呼び出しを views.ClassName.as_view() に変更
    # ------------------------------------------------------------------
    # サインアップ (views.pyで定義されていれば追加)
    # path('supporter/signup/',
    #      views.SupporterSignUpView.as_view(), # ★修正: views. を使い、ビュークラス名を明示
    #      name='supporter_signup'),
    
    # ログイン (auth_viewsなので変更なし)
    path('supporter/login/',
         auth_views.LoginView.as_view(template_name='supporter/login.html'),
         name='supporter_login'),

    # ログアウト (auth_viewsなので変更なし)
    path('supporter/logout/',
         auth_views.LogoutView.as_view(template_name='supporter/logout.html'),
         name='supporter_logout'),

]