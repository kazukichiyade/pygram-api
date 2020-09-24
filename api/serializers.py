from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile, Post, Comment

# 下記を担うのがシリアライザー
# DBへ格納する時は、指定されたデータ等を対象にvalidationを通してからDBへ格納
# DBから出力し表示する時は、表示項目の制限等を加えてJSON形式にてDBから出力


class UserSerializer(serializers.ModelSerializer):
    # Metaにオプションを定義
    class Meta:
        # Userモデル指定
        model = get_user_model()
        # 使用したいfield指定
        fields = ("id", "email", "password")
        # getメソッドを使用しても取得できないように設定
        extra_kwargs = {"password": {"write_only": True}}

    # validated_data:バリデーションを通過したデータを使用し、新規ユーザー作成
    def create(self, validated_data):
        # objects:UserManagerが格納されてあるのでcreate_userメソッドが使用できる
        user = get_user_model().objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    # formatで整形
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    # Metaにオプションを定義
    class Meta:
        # Profileモデル指定
        model = Profile
        # 使用したいfield指定
        fields = ("id", "nickName", "userProfile", "created_on", "img")
        # 自分自身のユーザープロフィールを自動で取得するように
        extra_kwargs = {"userProfile": {"read_only": True}}


class PostSerializer(serializers.ModelSerializer):
    # formatで整形
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    # Metaにオプションを定義
    class Meta:
        # Postモデル指定
        model = Post
        # 使用したいfield指定
        fields = ("id", "title", "userPost", "created_on", "img", "liked")
        # 自分自身の投稿を自動で取得するように
        extra_kwargs = {"userPost": {"read_only": True}}


class CommentSerializer(serializers.ModelSerializer):
    # Metaにオプションを定義
    class Meta:
        # Commentモデル指定
        model = Comment
        # 使用したいfield指定
        fields = ("id", "text", "userComment", "post")
        # 自分自身のコメントを自動で取得するように
        extra_kwargs = {"userComment": {"read_only": True}}
