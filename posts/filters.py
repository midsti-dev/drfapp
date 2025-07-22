import django_filters

from posts.models import Post


class PostsFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ["title", "owner", "owner__id"]
