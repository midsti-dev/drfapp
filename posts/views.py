from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import mixins
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from posts.filters import PostsFilter
from posts.models import Post, PostAttachment
from posts.serializers import PostSerializer, PostAttachmentSerializer
from posts.permissions import PostOwnerPermission
from posts.tasks import log_posts_opened


# Create your views here.

class PostsViewSet(
    ModelViewSet
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = PostsFilter

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        if self.action == "create":
            return [IsAuthenticated()]
        if self.action in ("retrieve", "update", "partial_update", "destroy"):
            return [PostOwnerPermission()]
        return [AllowAny()]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        log_posts_opened.delay()
        return response


@extend_schema_view(
    create=extend_schema(
        request=PostAttachmentSerializer,
        responses=PostAttachmentSerializer,
    )
)
class PostAttachmentViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = PostAttachment.objects.all()
    serializer_class = PostAttachmentSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        if self.action in ("create", "destroy", "update"):
            return [PostOwnerPermission()]
        return [AllowAny()]

# class PostListViewSet(
#     mixins.RetrieveModelMixin,
#     mixins.ListModelMixin,
#     GenericViewSet
# ):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


# class PostViewSet(
#     viewsets.ReadOnlyModelViewSet
# ):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#     def get_queryset(self):
#         pk = self.kwargs.get("pk")
#
#         if not pk:
#             return Post.objects.none()
#
#         return Post.objects.filter(pk=pk)
