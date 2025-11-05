# =======================================================================
# 修正後の enright/models.py の完全版
# =======================================================================
from django.db import models
# from accounts.models import CustomUser <-- この行は削除（循環参照回避）

class Category(models.Model):
    '''投稿する写真のカテゴリを管理するモデル'''
    title = models.CharField(
        verbose_name='カテゴリ', # フィールドのタイトル
        max_length=20)
    
    def __str__(self):
        return self.title
    
class PhotoPost(models.Model):
    '''投稿されたデータを管理するモデル'''
    
    # ★★★ 修正箇所: CustomUserを文字列で参照 ('アプリ名.モデル名') ★★★
    user = models.ForeignKey(
        'accounts.CustomUser', # <-- 文字列参照に変更
        verbose_name='ユーザー',
        on_delete=models.CASCADE
        )
        
    category = models.ForeignKey(
        Category,
        verbose_name='カテゴリ',
        on_delete=models.PROTECT
        )
    
    title = models.CharField(
        verbose_name='タイトル', # フィールドのタイトル
        max_length=200          # 最大文字数は200
        )
    comment = models.TextField(
        verbose_name='内容', 
        )
    # イメージのフィールド1
    image1 = models.ImageField(
        verbose_name='イメージ1', # フィールドのタイトル
        upload_to='photos',      # MEDIA_ROOT以下のphotosにファイルを保存
        )
    
    # イメージのフィールド2
    image2 = models.ImageField(
        verbose_name='イメージ2', # フィールドのタイトル
        upload_to='photos',      # MEDIA_ROOT以下のphotosにファイルを保存
        blank=True,              # フィールドの値は必須でない
        null=True                # データベースにnullが保存されることを許容
        )
    # 投稿日時のフィールド
    posted_at = models.DateTimeField(
        verbose_name='投稿日時', # フィールドのタイトル
        auto_now_add=True       # 日時を自動追加
        )
    
    def __str__(self):
        return self.title