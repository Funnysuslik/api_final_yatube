from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Post, Group, Follow, User


class PostsSerializer(serializers.ModelSerializer):
    """Serializer for Post model."""
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        fields = "__all__"
        model = Post


class CommentsSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )

    class Meta:
        fields = "__all__"
        model = Comment
        read_only_fields = ('post',)


class GroupsSerializer(serializers.ModelSerializer):
    """Serializer for Group model."""

    class Meta:
        model = Group
        fields = ("id", "title", "description")


class FollowsSerializer(serializers.ModelSerializer):
    """Serializer for Follow model."""
    user = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
    )

    class Meta:
        model = Follow
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]

    def validate(self, data):
        """Validates if user trying to follow himself."""
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'You can not follow yourself'
            )

        return data
