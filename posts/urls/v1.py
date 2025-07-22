from rest_framework.routers import DefaultRouter

from posts.views import PostsViewSet, PostAttachmentViewSet

router = DefaultRouter()

router.register("posts", PostsViewSet)
router.register("post_attachments", PostAttachmentViewSet)

urlpatterns = router.urls
