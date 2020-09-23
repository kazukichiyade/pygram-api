from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings


# username認証からemail認証に変更するため、BaseUserManagerをオーバーライド
class UserManager(BaseUserManager):

    # UserManager定義
    def create_user(self, email, password=None):

        if not email:
            raise ValueError("email is must")

        # インスタンス作成及びemail格納(取得したemailが大文字も小文字になるように設定)
        user = self.model(email=self.normalize_email(email))
        # パスワードをハッシュ化
        user.set_password(password)
        # DB保存
        user.save(using=self._db)

        return user

    # 管理者用のUserManager定義
    def create_superuser(self, email, password):
        # 通常のUserを作成
        user = self.create_user(email, password)
        # adminのダッシュボードにログインする権限付与
        user.is_staff = True
        # 管理者権限付与(DB変更等の全権限)
        user.is_superuser = True
        user.save(using=self._db)

        return user


# Userモデルを定義(usernameからemailにモデルの定義変更をするため、AbstractBaseUserをオーバーライド)
class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # インスタンス作成し、いつでもUserManagerクラスのメソッドを使用できるように設定
    objects = UserManager()

    # 初期状態では"username"になっている
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email
