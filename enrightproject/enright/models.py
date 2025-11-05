from django.db import models

# accountsアプリのmodelsモジュールからCustomUserをインポート
from accounts.models import CustomUser

class Category(models.Model):
    '''投稿する写真のカテゴリを管理するモデル
    '''
    # カテゴリ名のフィールド
    title = models.CharField(
        verbose_name='カテゴリ', # フィールドのタイトル
        max_length=20)
    def __str__(self):
        '''オブジェクトを文字列に変換して返す
        
        Returns(str):カテゴリ名
        '''
        return self.title
    
class PhotoPost(models.Model):
    '''投稿されたデータを管理するモデル
    '''
    # CustomUserモデル(のuser_id)とPhotoPostモデルを
    # 1対多の関係で結び付ける
    # CustomUserが親でPhotoPostが子の関係となる
    user = models.ForeignKey(
        CustomUser,
        # フィールドのタイトル
        verbose_name='ユーザー',
        # ユーザーを削除する場合はそのユーザーの投稿データもすべて削除する
        on_delete=models.CASCADE
        )
    # Categoryモデル(のtitle)とPhotoPostモデルを
    # 1対多の関係で結び付ける
    # Categoryが親でPhotoPostが子の関係となる
    category = models.ForeignKey(
        Category,
        # フィールドのタイトル
        verbose_name='カテゴリ',
        # カテゴリに関連付けられた投稿データが存在する場合は
        # そのカテゴリを削除出来ないようにする
        on_delete=models.PROTECT
        )
    # タイトル用のフィールド
    title = models.CharField(
        verbose_name='タイトル',# フィールドのタイトル
        max_length=200# 最大文字数は200
        )
    # 内容用のフィールド
    comment = models.TextField(
        verbose_name='内容', # フィールドのタイトル
        )
        
# イメージのフィールド1
    image1 = models.ImageField(
        verbose_name='写真1 (メイン)',
        upload_to='photos',# MEDIA_ROOT以下のphotosにファイルを保存
        # blank=False, # デフォルト値なので省略可能
        # null=False   # デフォルト値なので省略可能
    )
    
    # イメージのフィールド2 (既に非必須)
    image2 = models.ImageField(
        verbose_name='写真2', # フィールドのタイトルを'イメージ2'から変更
        upload_to='photos',# MEDIA_ROOT以下のphotosにファイルを保存
        blank=True,# フィールドの値は必須でない
        null=True# データベースにnullが保存されることを許容
        )
        
    # ★★★ 修正箇所2: image3、image4、image5 を追加 (非必須) ★★★
    image3 = models.ImageField(
        verbose_name='写真3',
        upload_to='photos',
        blank=True,
        null=True
    )
    image4 = models.ImageField(
        verbose_name='写真4',
        upload_to='photos',
        blank=True,
        null=True
    )
    image5 = models.ImageField(
        verbose_name='写真5',
        upload_to='photos',
        blank=True,
        null=True
    )

    # 投稿日時のフィールド
    posted_at = models.DateTimeField(
        verbose_name='投稿日時',# フィールドのタイトル
        auto_now_add=True# 日時を自動追加
        )
    
    def __str__(self):
        '''オブジェクトを文字列に変換して返す
        
        Returns(str):投稿記事のタイトル
        '''
        return self.title