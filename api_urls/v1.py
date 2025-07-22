from django.urls import path, include

urlpatterns = [
    path("", include("users.urls.v1")),
    path("", include("posts.urls.v1")),
]
