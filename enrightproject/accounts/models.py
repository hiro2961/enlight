from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    '''
    Userモデルを継承したカスタムユーザモデル
    '''
    
    # ★★★ ここから追加 ★★★
    
    # ユーザー種別の選択肢を定義
    USER_TYPE_CHOICES = (
        (1, '一般ユーザー'),
        (2, '要支援者'),
        (3, '支援者'), # 支援者は管理画面でのみ作成・設定
    )

    # ユーザー種別を保存するフィールド
    # default=1 で、新規ユーザーのデフォルトを「一般ユーザー」に設定
    user_type = models.PositiveSmallIntegerField(
        verbose_name='ユーザー種別',
        choices=USER_TYPE_CHOICES,
        default=1,
    )

    # ★★★ ここまで追加 ★★★
    
    # ★ リバースアクセサの競合を解消するため、related_nameを設定 ★
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=('The groups this user belongs to...'),
        related_name="rescue_user_set", # rescue_accounts固有の名前
        related_query_name="rescue_user",
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="rescue_user_permissions", # rescue_accounts固有の名前
        related_query_name="rescue_user_permission",
    )

    pass