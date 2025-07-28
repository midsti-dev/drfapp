from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from users.filters import UserFilter
from users.models import User
from users.permissions import IsOwner
from users.serializers import UserSerializer, UserCreateSerializer


# Create your views here.
class UserViewSet(
    ModelViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [
        DjangoFilterBackend,
        
    ]
    filterset_class = UserFilter

    def get_serializer_class(self):
        if self.action == "register":
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        if self.action in ("update", "partial_update", "destroy"):
            return [IsOwner()]
        if self.action == "register":
            return [AllowAny()]
        return [AllowAny()]

    @action(detail=False, methods=["post"])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserListAPIView(
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer


class UserUpdateAPIView(mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        GenericViewSet):
    # queryset = User.objects.()
    serializer_class = UserSerializer
    permission_classes = (IsOwner,)


