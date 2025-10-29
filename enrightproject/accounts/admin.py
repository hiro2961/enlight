from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    '''管理ページのレコード一覧に表示するカラムを設定するクラス'''
    
    # user_typeを削除し、is_staff (管理権限) のみで表示
    list_display = ('id', 'username', 'is_staff') 
    
    list_display_links = ('id', 'username')

    # user_typeを削除し、is_staff (管理権限) のみでフィルタリング
    list_filter = ('is_staff',) 

    search_fields = ('username',)

    # fieldsetsからも 'user_type' の行を削除（または正しいフィールド名に修正）
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('パーミッション', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        # ★★★ ここを修正 ★★★
        # アカウント種別フィールドが不明なため、一旦削除
        ('個人情報', {'fields': ('first_name', 'last_name', 'email')}),
        ('重要日付', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)