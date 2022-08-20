from django.urls import path, include
from rest_framework import routers
from .views import PostsViewSet, GroupsViewSet, CommentsViewSet, FollowsViewSet

app_name = "api"

router = routers.DefaultRouter()
router.register(r"posts", PostsViewSet)
router.register(r"groups", GroupsViewSet)
router.register(r"posts/(?P<post_id>\d+)/comments", CommentsViewSet)
router.register(r"follow", FollowsViewSet)

urlpatterns = [
    path("v1/", include("djoser.urls")),
    path("v1/", include("djoser.urls.jwt")),
    path("v1/", include(router.urls)),
]
