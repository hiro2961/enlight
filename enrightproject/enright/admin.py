from django.contrib import admin
from django.utils.html import format_html
from .models import Category, PhotoPost

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')

class PhotoPostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'user',
        'category',
        'thumbnail_preview',
        'posted_at',
    )
    list_display_links = ('id', 'title')
    list_filter = ('category', 'posted_at')
    search_fields = ('title', 'comment', 'user__username')
    autocomplete_fields = ('user',) 
    date_hierarchy = 'posted_at'
    
    readonly_fields = (
        'image1_preview', 
        'image2_preview', 
        'image3_preview', 
        'image4_preview', 
        'image5_preview',
        'posted_at'
    )
    
    fieldsets = (
        (None, {'fields': ('title', 'category', 'user')}),
        ('内容', {'fields': ('comment',)}),
        ('写真アップロード (最大5枚まで)', {
            'fields': (
                ('image1', 'image1_preview'),
                ('image2', 'image2_preview'),
                ('image3', 'image3_preview'),
                ('image4', 'image4_preview'),
                ('image5', 'image5_preview'),
            )
        }),
    )
    
    # ★追加: JSファイルを読み込むためのMediaクラス★
    class Media:
        # Step 1で作成したJSファイルのパスに合わせる！
        js = (
            'enlight/js/realtime_preview.js', 
        )

    # 一覧表示用のサムネイルプレビュー
    def thumbnail_preview(self, obj):
        if obj.image1:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.image1.url)
        return "No Image"
    thumbnail_preview.short_description = 'メイン画像プレビュー'

    # プレビュー表示用のHTMLのみを返すメソッド
    def _preview_html(self, obj, image_field_name):
        """プレビュー用のプレースホルダーと既存画像HTMLを返す"""
        preview_id = f'preview_{image_field_name}'
        
        # 既存の画像表示
        existing_html = ""
        image = getattr(obj, image_field_name) if obj else None
        if image and image.url:
            existing_html = f'<img id="{preview_id}_existing" src="{image.url}" style="max-width: 200px; height: auto; margin-bottom: 5px;" />'

        # リアルタイムプレビューが表示される場所
        live_html = f'<div id="{preview_id}_live"></div>'
        
        return format_html(existing_html + live_html)
        
    def image1_preview(self, obj):
        return self._preview_html(obj, 'image1')
    image1_preview.short_description = '写真1プレビュー'
    
    def image2_preview(self, obj):
        return self._preview_html(obj, 'image2')
    image2_preview.short_description = '写真2プレビュー'
    
    def image3_preview(self, obj):
        return self._preview_html(obj, 'image3')
    image3_preview.short_description = '写真3プレビュー'

    def image4_preview(self, obj):
        return self._preview_html(obj, 'image4')
    image4_preview.short_description = '写真4プレビュー'
    
    def image5_preview(self, obj):
        return self._preview_html(obj, 'image5')
    image5_preview.short_description = '写真5プレビュー'


admin.site.register(Category, CategoryAdmin)
admin.site.register(PhotoPost, PhotoPostAdmin)