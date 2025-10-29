from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    '''
    管理ページのレコード一覧に表示するカラムを設定するクラス
    '''
    # ★★★ 修正箇所 ★★★
    # list_displayに、表示したいカラム名（id, username, user_typeなど）を追加
    list_display = ('id', 'username', 'user_type', 'is_staff')
    
    # クリック可能なリンクを設定
    list_display_links = ('id', 'username')

    # user_typeでフィルタリングできるようにする
    list_filter = ('user_type', 'is_staff')

    # 検索フィールドの設定（usernameで検索可能に）
    search_fields = ('username',)

    # 詳細ページでのフィールドの表示順序とグルーピング（例）
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('パーミッション', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('アカウント情報', {'fields': ('user_type', 'first_name', 'last_name', 'email')}),
        ('重要日付', {'fields': ('last_login', 'date_joined')}),
    )
    # ★★★ 修正箇所 終了 ★★★

# Django管理サイトにCustomUser,CustomUserAdminを登録する
admin.site.register(CustomUser, CustomUserAdmin)