from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = "user"

# ModelViewSetを継承した場合
router = DefaultRouter()
router.register("profile", views.ProfileViewSet)
router.register("post", views.PostViewSet)
router.register("comment", views.CommentViewSet)

# 汎用APIViewを継承した場合
urlpatterns = [
    path("register/", views.CreateUserView.as_view(), name="register"),
    path("myprofile/", views.MyProfileListView.as_view(), name="myprofile"),
    path("", include(router.urls)),
]