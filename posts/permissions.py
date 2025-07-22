from rest_framework import permissions

from posts.models import PostAttachment, Post


class PostOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Post):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class PostAttachmentOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: PostAttachment):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.post.owner == request.user
