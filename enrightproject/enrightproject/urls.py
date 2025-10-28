"""enrightproject URL Configuration / photoproject URL Configuration の統合版"""
from django.contrib import admin
from django.urls import path, include 
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),

    # ------------------------------------------------------------------
    # 【メインアプリとアカウントアプリの参照】
    # ------------------------------------------------------------------
    # 1. メインアプリ (enright) - パスはそのまま '/'、名前空間は 'main'
    path('', include('enright.urls', namespace='main')), 

    # 2. 新しい統合アカウントアプリ (accounts) をインクルード
    #    パスプレフィックスなしでインクルードし、accounts/urls.py内で citizen/, rescue/ などのパスを定義
    path('', include('accounts.urls', namespace='accounts')), # ★★★ 修正箇所 ★★★
    
    # ------------------------------------------------------------------
    # 【パスワードリセットURL】
    # ------------------------------------------------------------------
    # パスワードリセット申し込みページ
    path('password_reset/',
          auth_views.PasswordResetView.as_view(
              template_name = "password_reset.html"),
          name = 'password_reset'),
    
    # メール送信完了ページ
    path('password_reset/done/',
          auth_views.PasswordResetDoneView.as_view(
              template_name = "password_reset_sent.html"),
          name ='password_reset_done'),
    
    # パスワードリセットページ
    path('reset/<uidb64>/<token>',
          auth_views.PasswordResetConfirmView.as_view(
              template_name = "password_reset_form.html"),
          name ='password_reset_confirm'),

    # パスワードリセット完了ページ
    path('reset/done/',
          auth_views.PasswordResetCompleteView.as_view(
              template_name = "password_reset_done.html"),
          name ='password_reset_complete'),
]

# urlpatternsにmediaフォルダーのURLパターンを追加 (変更なし)
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)