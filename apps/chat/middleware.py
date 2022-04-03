from rest_framework_simplejwt.tokens import UntypedToken
from django.db import close_old_connections
from urllib.parse import parse_qs
from django.conf import settings
from django.contrib.auth import get_user_model
from jwt import decode as jwt_decode
from channels.db import database_sync_to_async


@database_sync_to_async
def get_user(user_id):
    # Get the user using ID
    user = get_user_model().objects.get(id=user_id)
    return user


class TokenAuthMiddleware:
    """
    Custom token auth middleware
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):

        # Close old database connections to prevent usage of timed out connections
        close_old_connections()

        # Get the token
        try:
            access_token = parse_qs(scope["query_string"].decode("utf8")).get('token')[
                0
            ]
            UntypedToken(access_token)
        except Exception as e:
            # scope['error'] = 'Invalid token'
            return None
        else:
            #  Then token is valid, decode it
            decoded_data = jwt_decode(
                access_token, settings.SECRET_KEY, algorithms=["HS256"]
            )

            # Get the user using ID
            scope['user'] = await get_user(decoded_data["user_id"])
            print(scope['user'])

        return await self.app(scope, receive, send)
