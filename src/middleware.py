from urllib.parse import parse_qs

from channels.auth import AuthMiddlewareStack
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User  # adjust your user model import
import jwt
from django.conf import settings
from asgiref.sync import sync_to_async


@sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode()
        query_params = parse_qs(query_string)
        token = query_params.get("token")

        if token:
            try:
                access_token = AccessToken(token[0])
                user = await get_user(access_token["user_id"])
                scope["user"] = user
            except jwt.ExpiredSignatureError:
                scope["user"] = AnonymousUser()
            except jwt.InvalidTokenError:
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)


def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(AuthMiddlewareStack(inner))
