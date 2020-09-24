from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from . import serializers
from .models import Profile, Post, Comment


# 新規ユーザー作成に特化した汎用APIView
class CreateUserView(generics.CreateAPIView):
    # シリアライザー指定
    serializer_class = serializers.UserSerializer
    # 現在permission_classesはjwtを使用する事になっているが、
    # 新規ユーザー作成の場合認証されていないユーザーも触るのでAllowAnyで誰でもアクセスできるように認証を上書き
    permission_classes = (AllowAny,)


# Profileモデルに対応させたModelViewSet(CRUD対応できるように)
class ProfileViewSet(viewsets.ModelViewSet):
    # Profileのオブジェクトを全て取得
    queryset = Profile.objects.all()
    # シリアライザー指定
    serializer_class = serializers.ProfileSerializer

    # serializers.pyで指定した自分自身のユーザープロフィールを取得できるように設定
    def perform_create(self, serializer):
        serializer.save(userProfile=self.request.user)


# ログインしているユーザーのViewを取得(ListAPIView:取得に特化)
class MyProfileListView(generics.ListAPIView):
    # Profileのオブジェクトを全て取得
    queryset = Profile.objects.all()
    # シリアライザー指定
    serializer_class = serializers.ProfileSerializer

    # ログインしているユーザー自身のプロフィールを取得するように設定(read_onlyにした箇所の対応)
    def get_queryset(self):
        return self.queryset.filter(userProfile=self.request.user)


# Postモデルに対応させたModelViewSet(CRUD対応できるように)
class PostViewSet(viewsets.ModelViewSet):
    # Postのオブジェクトを全て取得
    queryset = Post.objects.all()
    # シリアライザー指定
    serializer_class = serializers.PostSerializer

    # ログインしているユーザー自身の投稿を取得するように設定
    def perform_create(self, serializer):
        serializer.save(userPost=self.request.user)


# Commentモデルに対応させたModelViewSet(CRUD対応できるように)
class CommentViewSet(viewsets.ModelViewSet):
    # Postのオブジェクトを全て取得
    queryset = Comment.objects.all()
    # シリアライザー指定
    serializer_class = serializers.CommentSerializer

    # ログインしているユーザー自身のコメントを取得するように設定
    def perform_create(self, serializer):
        serializer.save(userComment=self.request.user)