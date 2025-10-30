from django.contrib import admin
from .models import Category, PhotoPost

class CategoryAdmin(admin.ModelAdmin):
    '''管理ページのレコード一覧の表示するカラムを設定するクラス
    '''
    # レコード一覧にidとtitleを表示
    list_display = ('id', 'title')
    # 表示するカラムにリンクを設定
    list_display_links = ('id', 'title')

# --- PhotoPostAdmin の修正（一覧表示の強化とユーザーフィルタ対策） ---
class PhotoPostAdmin(admin.ModelAdmin):
    '''管理ページのレコード一覧の表示するカラムを設定するクラス
    '''
    # 1. 一覧ページに表示するフィールド（列）を詳細化
    list_display = (
        'id',           # ID
        'title',        # タイトル
        'user',         # 投稿者
        'category',     # カテゴリ
        'posted_at',    # 投稿日時
    )
    
    # 表示するカラムにリンクを設定
    list_display_links = ('id', 'title')
    
    # 2. フィルタリング機能
    # ユーザー数が多くなるため 'user' フィルタは削除し、カテゴリと日時のみ残す
    list_filter = (
        'category',     # カテゴリで絞り込む
        'posted_at'     # 投稿日時で絞り込む
    )
    
    # 3. 検索窓機能（タイトル、内容、投稿者名で検索可能）
    search_fields = (
        'title',        
        'comment',      
        'user__username' # 投稿者名（ユーザーモデルのusername属性）で検索
    )
    
    # 4. ★ユーザー数増加対策：編集画面でのユーザー選択を検索ベースにする★
    # これにより、一覧画面のサイドバーにユーザーの長いリストは表示されません。
    autocomplete_fields = ('user',) 
    
    # 5. 日付によるクイックナビゲーション
    date_hierarchy = 'posted_at'

# Django管理サイトにCategory、CategoryAdminを登録する
admin.site.register(Category, CategoryAdmin)

# Django管理サイトにPhotoPost、PhotoPostAdminを登録する
admin.site.register(PhotoPost, PhotoPostAdmin)