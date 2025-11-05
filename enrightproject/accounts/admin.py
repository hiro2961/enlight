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

    # 基本のfieldsetsを定義
    base_fieldsets = (
        (None, {'fields': ('username', 'password')}), # パスワードハッシュ化に対応
        ('ユーザー種別', {'fields': ('user_type',)}),
        ('個人情報', {'fields': ('first_name', 'last_name', 'email')}),
        ('パーミッション', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('重要日付', {'fields': ('last_login', 'date_joined')}),
    )

    # 資格情報フィールドのみを持つfieldsets
    qualification_fieldset = ('資格情報', {'fields': ('qualification_details',)})

    # ★★★ 修正箇所: get_fieldsetsメソッドのロジックを修正 ★★★
    def get_fieldsets(self, request, obj=None):
        """
        ユーザー種別に応じて表示するfieldsetsを切り替える
        obj: 編集中のインスタンス (新規作成時はNone)
        """
        # 既存ユーザーを編集していて、そのユーザーが「支援者」（user_type=3）の場合
        is_helper = obj and obj.user_type == 3

        # 新規作成時、または既存ユーザーが支援者の場合に資格欄を追加
        if obj is None or is_helper:
            
            # 新規作成時は、ユーザータイプを「支援者」に設定できるように、fieldsetsをカスタマイズする
            # 資格情報欄を組み込むために、base_fieldsetsをコピー
            fieldsets_list = list(self.base_fieldsets)
            
            # 資格情報欄をユーザー種別の直後（インデックス2）に挿入
            fieldsets_list.insert(2, self.qualification_fieldset) 
            
            # 新規作成時はパスワードのハッシュ化用フォームを使いたいため、
            # get_fieldsetsの戻り値としてfieldsetsをUserAdminから取得し、カスタマイズする
            if obj is None:
                # UserAdminのfieldsetsを取得（新規作成用のパスワードフィールドを含む）
                user_admin_fieldsets = super().get_fieldsets(request, obj)
                # 資格情報欄を組み込むために、fieldsets_listを再構成
                
                # 新規作成時フォームの基本設定（パスワード設定部分を含む）をコピー
                new_fieldsets = list(user_admin_fieldsets)
                
                # ユーザー種別と個人情報の間に資格情報を挿入するためのロジック
                # ここで資格情報を追加したい場所を見つけるために、タプルの名前で検索する
                insert_index = -1
                for i, (name, options) in enumerate(new_fieldsets):
                    if name == 'Personal info' or name == '個人情報': # Personal info または対応する日本語名
                         insert_index = i

                if insert_index != -1:
                    new_fieldsets.insert(insert_index, self.qualification_fieldset)
                    
                # 新規作成時はuser_typeがデフォルトで1になるため、手動でユーザー種別欄をカスタマイズする必要がある
                # ただし、UserAdminを継承しているため、既存のfieldsetsを使用し、資格欄のみを挿入するのが安全
                return tuple(new_fieldsets)
            
            # 既存の支援者を編集する場合は、カスタマイズしたfieldsetsを返す
            return tuple(fieldsets_list)

        # 支援者以外のユーザー（一般、要支援者、管理者）を編集する場合
        else:
            return self.base_fieldsets

    # パスワードハッシュ化用のフィールドを設定
    def get_form(self, request, obj=None, **kwargs):
        # UserAdminのデフォルトフォームを使用
        return super().get_form(request, obj, **kwargs)
    
# Django管理サイトにCustomUser,CustomUserAdminを登録する
admin.site.register(CustomUser, CustomUserAdmin)