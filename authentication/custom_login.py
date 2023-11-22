from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from api.models import Usr


class CustomUserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        if '@' in username:
            kwargs = {'email__iexact': username}
        else:
            kwargs = {'username__iexact': username}
        try:
            user = Usr.objects.get(**kwargs)
            if check_password(password, user.password):
                return user
        except Usr.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Usr.objects.get(pk=user_id)
        except Usr.DoesNotExist:
            return None
