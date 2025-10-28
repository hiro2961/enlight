from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
# ↑ GroupとPermissionのインポートが必要です

class CustomUser(AbstractUser):
    '''
    Userモデルを継承したカスタムユーザモデル
    '''
    
    # ★ リバースアクセサの競合を解消するため、related_nameを設定 ★
    
    # groupsフィールド
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=('The groups this user belongs to...'),
        related_name="rescue_user_set", # rescue_accounts固有の名前
        related_query_name="rescue_user",
    )
    
    # user_permissionsフィールド
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="rescue_user_permissions", # rescue_accounts固有の名前
        related_query_name="rescue_user_permission",
    )

    pass