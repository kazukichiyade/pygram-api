from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings


# アバター画像アップロード時拡張子取得及びファイル名作成
def upload_avatar_path(instance, filename):
    ext = filename.split(".")[-1]
    return "/".join(
        [
            "avatars",
            str(instance.userProfile.id) + str(instance.nickName) + str(".") + str(ext),
        ]
    )


# 投稿画像アップロード時拡張子取得及びファイル名作成
def upload_post_path(instance, filename):
    ext = filename.split(".")[-1]
    return "/".join(
        ["posts", str(instance.userPost.id) + str(instance.title) + str(".") + str(ext)]
    )


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


# Profileモデルを定義
class Profile(models.Model):
    nickName = models.CharField(max_length=20)
    # 一対一及び対象のユーザーが削除された場合userProfileも連動して削除
    userProfile = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="userProfile", on_delete=models.CASCADE
    )
    # 初回登録時日時は自動で登録
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)

    def __str__(self):
        return self.nickName


# Postモデル定義
class Post(models.Model):
    title = models.CharField(max_length=100)
    # 投稿者(一対多及び対象のユーザーが削除された場合userPostも連動して削除)
    userPost = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="userPost", on_delete=models.CASCADE
    )
    # 初回登録時日時は自動で登録
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_post_path)
    # 多対多
    liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked", blank=True
    )

    def __str__(self):
        return self.title


# コメントモデル定義
class Comment(models.Model):
    text = models.CharField(max_length=100)
    # どのユーザーに対してのコメントなのか(一対多及び対象のユーザーが削除された場合userCommentも連動して削除)
    userComment = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="userComment", on_delete=models.CASCADE
    )
    # 一対多及び対象のユーザーが削除された場合userCommentも連動して削除
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text