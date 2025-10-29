from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import CustomUser

# CustomUserAdminをUserAdminから継承
class CustomUserAdmin(UserAdmin): 
    '''
    管理ページのレコード一覧に表示、フィルタリング、検索などを設定する
    （UserAdminを継承してパスワードハッシュ化に対応）
    '''
    # レコード一覧に表示
    list_display = ('id', 'username', 'user_type', 'is_staff')
    
    # クリック可能なリンク
    list_display_links = ('id', 'username')

    # フィルタリング
    list_filter = ('user_type', 'is_staff')

    # 検索
    search_fields = ('username', 'email')

    # 詳細ページでのフィールドの表示順序とグルーピング
    fieldsets = (
        (None, {'fields': ('username', 'password')}), # パスワードハッシュ化に対応
        ('ユーザー種別', {'fields': ('user_type',)}),
        # ★★★ 資格情報フィールドをfieldsetsに組み込む ★★★
        ('資格情報', {'fields': ('qualification_details',)}),
        # ★★★ ここまで ★★★
        ('個人情報', {'fields': ('first_name', 'last_name', 'email')}),
        ('パーミッション', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('重要日付', {'fields': ('last_login', 'date_joined')}),
    )
    
# Django管理サイトにCustomUser,CustomUserAdminを登録する
admin.site.register(CustomUser, CustomUserAdmin)