from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
# ↑ GroupとPermissionのインポートが必要です

class CustomUser(AbstractUser):
    '''
    Userモデルを継承したカスタムユーザモデル
    '''
    
    # ユーザー種別の選択肢を定義
    USER_TYPE_CHOICES = (
        (1, '一般ユーザー'),
        (2, '要支援者'),
        (3, '支援者'), 
        (4, '管理者'),
    )

    # ユーザー種別を保存するフィールド
    user_type = models.PositiveSmallIntegerField(
        verbose_name='ユーザー種別',
        choices=USER_TYPE_CHOICES,
        default=1,
    )

    # 資格情報フィールド
    qualification_details = models.TextField(
        verbose_name='所持資格',
        blank=True,
        null=True,
        help_text='支援者が所持している資格を記載してください。'
    )
    
    # ★★★ 修正箇所1: emailフィールドをユニークにする ★★★
    # AbstractUserのemailをオーバーライドし、unique=Trueを設定
    email = models.EmailField(
        'email address',
        unique=True,
        blank=False,
    )
    
    # ★★★ 修正箇所2: ログインに使うフィールドをメールアドレスに変更 ★★★
    USERNAME_FIELD = 'email'
    
    # ★★★ 修正箇所3: ユーザー作成時に必須とするフィールドを設定 ★★★
    # emailがUSERNAME_FIELDになったため、REQUIRED_FIELDSからemailを除外します
    # ここでは既存のusernameを必須として残しますが、必要に応じてfirst_name, last_name等を追加してください。
    REQUIRED_FIELDS = ['username']
    
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

    pass # (CustomUserクラスの終わり)