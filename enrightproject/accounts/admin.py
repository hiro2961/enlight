from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import CustomUser

# CustomUserAdminをUserAdminから継承
class CustomUserAdmin(UserAdmin): 
    '''
    管理ページのレコード一覧に表示、フィルタリング、検索などを設定し、
    特定のフィールドをユーザー種別に応じて表示する
    '''
    # レコード一覧に表示
    list_display = ('id', 'username', 'user_type', 'is_staff')
    list_display_links = ('id', 'username')
    list_filter = ('user_type', 'is_staff')
    search_fields = ('username', 'email')

    # 基本のfieldsetsを定義 (UserAdminのものを簡略化してCustomUser向けに再定義)
    base_fieldsets = (
        (None, {'fields': ('username', 'password')}), # パスワードハッシュ化に対応
        ('ユーザー種別', {'fields': ('user_type',)}),
        ('個人情報', {'fields': ('first_name', 'last_name', 'email')}),
        ('パーミッション', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('重要日付', {'fields': ('last_login', 'date_joined')}),
    )

    # ★★★ 修正箇所: get_fieldsetsメソッドをオーバーライド ★★★
    def get_fieldsets(self, request, obj=None):
        """
        ユーザー種別に応じて表示するfieldsetsを切り替える
        obj: 編集中のインスタンス (新規作成時はNone)
        """
        # 新規作成時、または既存ユーザーのuser_typeが3（支援者）の場合
        if obj is None or obj.user_type == 3:
            # 基本のfieldsetsの先頭要素をコピーして、資格情報フィールドを追加
            # fieldsetsはタプルのリストなので、操作が少し複雑になる
            
            # base_fieldsetsをリストに変換して操作
            fieldsets_list = list(self.base_fieldsets)
            
            # 資格情報フィールドのタプルを作成し、user_typeの直後に追加
            qualification_fieldset = ('資格情報', {'fields': ('qualification_details',)})
            fieldsets_list.insert(2, qualification_fieldset) # 2番目 (インデックス2) に挿入

            return tuple(fieldsets_list)
        
        # 支援者以外のユーザー（一般、要支援者）の場合
        else:
            return self.base_fieldsets
    # ★★★ 修正箇所ここまで ★★★

# Django管理サイトにCustomUser,CustomUserAdminを登録する
admin.site.register(CustomUser, CustomUserAdmin)