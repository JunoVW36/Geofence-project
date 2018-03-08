from django.contrib.auth.backends import ModelBackend
from django.db import models
from datalive_auth.models import DataliveUser


class UsernameOrEmailBackend(ModelBackend):

    # this is the custom method called to authenticate a user
    def authenticate(self, request, username=None, email=None, password=None,
                     **kwargs):
        try:
            user = DataliveUser.objects.get(
                models.Q(username=username) | models.Q(email=username) |
                models.Q(email=email)
            )
        except DataliveUser.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            DataliveUser().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
