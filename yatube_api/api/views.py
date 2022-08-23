from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Post, Comment, Group
from .permissions import IsAuthenticatedAuthorOrReadOnly
from .serializers import (
    PostsSerializer,
    CommentsSerializer,
    GroupsSerializer,
    FollowsSerializer,
)


class PostsViewSet(viewsets.ModelViewSet):
    """ViewSet for Post model."""
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    permission_classes = [IsAuthenticatedAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentsViewSet(viewsets.ModelViewSet):
    """ViewSet for Comment model."""
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticatedAuthorOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        new_post = get_object_or_404(Post, pk=post_id)

        return Comment.objects.filter(post=new_post)

    def perform_create(self, serializer):
        commented_post = get_object_or_404(
            Post, pk=self.kwargs.get("post_id"))
        serializer.save(author=self.request.user, post=commented_post)


class GroupsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Group model."""
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer
    permission_classes = [
        IsAuthenticatedAuthorOrReadOnly,
    ]


class FollowsViewSet(viewsets.ModelViewSet):
    """ViewSet for Follow model."""
    serializer_class = FollowsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_fields = ("following__username",)

    def get_queryset(self):

        return self.request.user.follower

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
