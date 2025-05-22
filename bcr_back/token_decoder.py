import jwt
from django.conf import settings
from django.contrib.auth.models import User as authUser


class JWTTokenDecoder():
    token = ""

    def __init__(self, request):
        try:
            self.token = request.headers.get("Authorization")
        except Exception as e:
            self.token = ""

    def getUserFromToken(self):
        if self.token is None or self.token == "":
            return None
        try:
            decodedPayload = jwt.decode(self.token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = decodedPayload.get("user_id")
            auth_user = authUser.objects.get(id=user_id)
            return auth_user
        except Exception as e:
            return None
