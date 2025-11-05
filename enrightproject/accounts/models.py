# =======================================================================
# 修正後の accounts/models.py の完全版
# =======================================================================
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    '''
    Userモデルを継承したカスタムユーザモデル
    '''
    
    # 既存の 'auth.User' との関連名の競合を避けるための設定
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=('The groups this user belongs to...'),
        related_name="rescue_user_set", 
        related_query_name="rescue_user",
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="rescue_user_permissions", 
        related_query_name="rescue_user_permission",
    )

    pass