from django.contrib import admin
# ★UserAdminをインポートする★
from django.contrib.auth.admin import UserAdmin 
from .models import CustomUser

# CustomUserAdminをUserAdminから継承するように変更
class CustomUserAdmin(UserAdmin): 
    '''
    管理ページのレコード一覧に表示、フィルタリング、検索などを設定する
    （UserAdminを継承してパスワードハッシュ化に対応）
    '''
    # レコード一覧にid, username, user_type, is_staffを表示
    list_display = ('id', 'username', 'user_type', 'is_staff')
    
    # 表示するカラムにリンクを設定
    list_display_links = ('id', 'username')

    # user_typeとis_staffでフィルタリング可能に
    list_filter = ('user_type', 'is_staff')

    # 検索フィールドの設定
    search_fields = ('username', 'email')

    # 詳細ページでのフィールドの表示順序とグルーピングを整理
    # ★UserAdminのfieldsetsをオーバーライドして、user_typeなどを組み込む★
    fieldsets = (
        (None, {'fields': ('username', 'password')}), # パスワードを自動ハッシュ化するフォームを使用
        ('ユーザー種別', {'fields': ('user_type',)}),
        ('パーミッション', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('個人情報', {'fields': ('first_name', 'last_name', 'email')}),
        ('重要日付', {'fields': ('last_login', 'date_joined')}),
    )
    
# Django管理サイトにCustomUser,CustomUserAdminを登録する
admin.site.register(CustomUser, CustomUserAdmin)