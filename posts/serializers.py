from rest_framework import serializers

from posts.models import Post, PostAttachment
from users.serializers import UserPostSerializer


class PostSerializer(serializers.ModelSerializer):
    owner = UserPostSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ("title", "content", "owner")

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class PostAttachmentSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = PostAttachment
        fields = ("post", "caption", "image")
